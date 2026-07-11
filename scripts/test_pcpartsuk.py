import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import scrape_product_list
import logging

logging.basicConfig(level=logging.INFO)

products = scrape_product_list('cpus', max_pages=1)
print(f'Found {len(products)} CPUs')
for p in products[:5]:
    print(f'  {p["name"][:80]} - £{p["price"]} - {p["manufacturer"]}')