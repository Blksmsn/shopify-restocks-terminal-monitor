import requests
from bs4 import BeautifulSoup as Soup
import time
import logging

# Setup logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

url_list = ['https://www.dtlr.com/sitemap_products_1.xml?from=4185404702799&to=4187076657231',
            'https://stashedsf.com/sitemap_products_1.xml?from=212422295578&to=7153852514378',
            'https://kith.com/sitemap_products_1.xml?from=135297231&to=1844136869957',
            'https://shopnicekicks.com/sitemap_products_1.xml?from=1169123841&to=6786418442445',
            'https://store.unionlosangeles.com/sitemap_products_1.xml?from=4827046510669&to=6867702644813', 'https://www.thedarksideinitiative.com/sitemap_products_1.xml?from=11713616533&to=6956179357750', 'https://shop.atlasskateboarding.com/sitemap_products_1.xml?from=8529100305&to=6661279580256', 'https://lustmexico.com/sitemap_products_1.xml?from=1873592352811&to=6923415584834', 'https://www.apbstore.com/sitemap_products_1.xml?from=1038550171684&to=7280236789796', 'https://shop-us.doverstreetmarket.com/sitemap_products_1.xml?from=6295936499864&to=7152265429254', 'https://www.soleplayatl.com/sitemap_products_1.xml?from=2156691488864&to=8008634433687', 'https://two18.com/sitemap_products_1.xml?from=7139702997181&to=7476440629437', 'https://cncpts.com/sitemap_products_1.xml?from=1757246718021&to=6987936366655', 'https://www.atmosusa.com/sitemap_products_1.xml?from=4591390523444&to=7098738245684', 'https://undefeated.com/sitemap_products_1.xml?from=1306163183689&to=6678532653317', 'https://extrabutterny.com/sitemap_products_1.xml?from=279284877&to=1398136242224', 'https://www.shoepalace.com/sitemap_products_1.xml?from=4631208525870&to=6835360858318', 'https://stay-rooted.com/sitemap_products_1.xml?from=8036261776&to=6891117772823', 'https://www.theclosetinc.com/sitemap_products_1.xml?from=2064338223202&to=6870755737698', 'https://www.saintalfred.com/sitemap_products_1.xml?from=269030965&to=7136102219820', 'https://feature.com/sitemap_products_1.xml?from=289401889&to=1785276891207', 'https://drakerelated.com/sitemap_products_1.xml?from=6997065859254&to=7594585063606', 'https://gallery.canary---yellow.com/sitemap_products_1.xml?from=2063933177905&to=7449783664832', 'https://www.soleclassics.com/sitemap_products_1.xml?from=271321905&to=7333933252791', 'https://www.slamcity.com/sitemap_products_1.xml?from=1531719286854&to=4659593543750', 'https://corporategotem.com/sitemap_products_1.xml?from=4417893007404&to=7364873126046', 'https://thepremierstore.com/sitemap_products_1.xml?from=7383707971&to=6669797818433', 'https://gbny.com/sitemap_products_1.xml?from=6256257991&to=6641754013792', 'https://packershoes.com/sitemap_products_1.xml?from=10927139795&to=7267163308121', 'https://www.alumniofny.com/sitemap_products_1.xml?from=2414023934036&to=6830111916116', 'https://www.a-ma-maniere.com/sitemap_products_1.xml?from=4695354179683&to=7295187714229', 'https://www.socialstatuspgh.com/sitemap_products_1.xml?from=4472921423914&to=6901173092394', 'https://www.jjjjound.com/sitemap_products_1.xml?from=501973507&to=7118883684422', 'https://www.onenessboutique.com/sitemap_products_1.xml?from=184527205&to=6600559329364', 'https://www.trophyroomstore.com/sitemap_products_1.xml?from=8891412946&to=6868764098638']

keywords = ['nike-air-max-1-87', 'air-max-1-premium', 'w-nike-air-max-1-87', 'womens-nike-air-max-1-87', 'air-max-1-87' 'air-jordan-1', 'w-air-jordan-1', 'jordan-air-ship', 'air-jordan-1-low-og', 'air-jordan-2', 'w-air-jordan2', 'air-jordan-x-off-white-2' 'air-jordan-3', 'w-air-jordan-3', 'air-jordan-4', 'w-air-jordan-4' 'air-jordan-5', 'w-air-jordan-5', 'air-jordan-6', 'w-air-jordan-6', 'air-jordan-7', 'w-air-jordan-7', 'air-jordan-6-toro', 'nike-lebron-xx', 'nike-lebron-nxxt-gen', 'nike-dunk', 'womens-air-jordan-1',
            'womens-nike-dunk-low', 'nike-dunk-low', 'nike-dunk-low-retro', 'nike-dunk-low-co-jp', 'nike-dunk-low-co', 'nike-dunk-low-co-jp-snakeskin', 'nike-sb-blazer', 'nike-dunk-high', 'nike-sb-dunk-high', 'nike-sb-ishod', 'nike-ja-1-hunger', 'salehe-bembury', 'yeezy', 'adidas-campus', 'adidas-gazelle', 'crocs-pollex-slides', 'crocs-pollex-slide', 'clot-fragment-dunk-low', 'clot-nike-dunk-low', 'fragment-dunk-low', 'dtlr-new-balance-2002r-lovers-only', 'new-balance-2002r', 'new-balance-550', 'new-balance-9060', 'new-balance-990', 'new-balance-993', 'air-drake', 'nb-bb50', 'reebok-npc-ii', 'new-balance-uk-991', 'reebok-club-c-jjjjound']
items = []

# Flag to indicate if it's the first run
first_run = True

while True:
    for url_str in url_list:
        try:
            response = requests.get(url_str, timeout=100)
            soup = Soup(response.content, 'xml')
            urls = soup.findAll('url')

            # Temporarily store new items
            new_items = []

            for url in urls:
                link = url.find('loc').string
                if any(keyword in link for keyword in keywords):
                    # Add link to new items if not already present in items
                    if link not in items:
                        new_items.append(link)

            # If there are new items, add them to items and log them
            if new_items:
                for item in new_items:
                    items.append(item)
                    # Only log if it's not the first run
                    if not first_run:
                        print(f"🚨Item Recently Updated:\n{item}")
                        logging.info(f"Item Recently Updated: {item}")
            elif not first_run:
                logging.info(f"No new items found on {url_str}.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error while trying to get {url_str}: {e}")
            continue

    # Set first_run to False after the first run
    if first_run:
        print('The restock monitor has started...')
        first_run = False

    # Wait for 60 seconds before the next check
    print('Taking a break for 60 seconds...')
    time.sleep(60)
