import asyncio
import aiohttp
from bs4 import BeautifulSoup as Soup
import logging
import json
from typing import List, Dict
import aiosqlite
from aiolimiter import AsyncLimiter

# Setup logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

URL_LIST: List[str] = config['url_list']
KEYWORDS: List[str] = config['keywords']
DB_NAME: str = 'items.db'
RATE_LIMIT: int = 5  # requests per second

async def create_table() -> None:
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS items
            (url TEXT PRIMARY KEY, first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
        await db.commit()

async def is_new_item(db: aiosqlite.Connection, url: str) -> bool:
    async with db.execute('SELECT 1 FROM items WHERE url = ?', (url,)) as cursor:
        return await cursor.fetchone() is None

async def add_item(db: aiosqlite.Connection, url: str) -> None:
    await db.execute('INSERT OR IGNORE INTO items (url) VALUES (?)', (url,))
    await db.commit()

async def process_url(session: aiohttp.ClientSession, url: str, db: aiosqlite.Connection, limiter: AsyncLimiter) -> None:
    async with limiter:
        try:
            async with session.get(url, timeout=100) as response:
                soup = Soup(await response.text(), 'xml')
                urls = soup.findAll('url')

                for url_tag in urls:
                    link = url_tag.find('loc').string
                    if any(keyword in link for keyword in KEYWORDS):
                        if await is_new_item(db, link):
                            await add_item(db, link)
                            logging.info(f"🚨 New item found: {link}")
                        else:
                            logging.debug(f"Existing item: {link}")

        except asyncio.TimeoutError:
            logging.error(f"Timeout while processing {url}")
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")

async def main() -> None:
    await create_table()
    limiter = AsyncLimiter(RATE_LIMIT)

    while True:
        async with aiohttp.ClientSession() as session, aiosqlite.connect(DB_NAME) as db:
            tasks = [process_url(session, url, db, limiter) for url in URL_LIST]
            await asyncio.gather(*tasks)

        logging.info("Waiting for 60 seconds before next check...")
        await asyncio.sleep(60)

if __name__ == "__main__":
    logging.info("Restock monitor started...")
    asyncio.run(main())