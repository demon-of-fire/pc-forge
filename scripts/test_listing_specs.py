import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import scrape_category

products = scrape_category('psus', max_pages=1)
print(f'Found {len(products)} PSUs')
for p in products[:3]:
    print(f'  {p["name"]} - £{p["price"]} - {p["specs"]}')