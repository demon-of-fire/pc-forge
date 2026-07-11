import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import scrape_product_list

# Test with detail fetching for a few products
products = scrape_product_list('cpus', max_pages=1, fetch_details=True)
print(f'Found {len(products)} CPUs')
for p in products[:5]:
    print(f'  {p["name"]} - £{p["price"]} - specs: {p["specs"]}')