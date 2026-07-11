import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

soup = fetch_page('https://pcparts.uk/browse/cpus')
if soup:
    links = soup.select("a[href^='/product/']")
    from collections import defaultdict
    grouped = defaultdict(list)
    for link in links:
        pid = link.get("data-product-id")
        if pid:
            grouped[pid].append(link)
    
    # Check first 3 products' name elements
    for pid, elements in list(grouped.items())[:3]:
        print(f"\n=== Product {pid} ===")
        for i, el in enumerate(elements):
            text = el.get_text(strip=True)
            print(f"  Element {i}: '{text[:150]}'")