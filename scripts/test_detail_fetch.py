import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import scrape_product_list

# Test with detail fetching for just 2 CPUs
products = scrape_product_list('cpus', max_pages=1, fetch_details=True)
print(f'Found {len(products)} CPUs')
for p in products[:3]:
    print(f'  {p["name"]} - £{p["price"]} - {p["manufacturer"]}')
    print(f'    Specs: {p["specs"]}')