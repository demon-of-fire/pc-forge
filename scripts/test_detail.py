import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

# Test detail page extraction
from scrapers.pcpartsuk import extract_specs_from_detail_page

# Test CPU detail page
soup = fetch_page('https://pcparts.uk/product/22628/intel-core-i9-14900k-24-core-32-thread-up-to-6ghz-bx8071514900k')
if soup:
    specs = extract_specs_from_detail_page('cpus', soup)
    print("CPU Detail Specs:")
    for k, v in specs.items():
        print(f"  {k}: {v}")
else:
    print("Failed to fetch CPU detail page")

# Test GPU detail page
soup = fetch_page('https://pcparts.uk/product/21922/msi-geforce-rtx-3050-ventus-2x-xs-oc-8gb-gddr6-gra-geforce-rtx-3050-ventus-2x-xs-8g-oc')
if soup:
    specs = extract_specs_from_detail_page('gpus', soup)
    print("\nGPU Detail Specs:")
    for k, v in specs.items():
        print(f"  {k}: {v}")
else:
    print("Failed to fetch GPU detail page")