import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

soup = fetch_page('https://pcparts.uk/browse/cpus')
if soup:
    # Find containers - maybe there's a wrapper div
    cards = soup.select("a[href^='/product/']")
    
    # Group by data-product-id
    from collections import defaultdict
    grouped = defaultdict(list)
    for card in cards:
        pid = card.get('data-product-id')
        if pid:
            grouped[pid].append(card)
    
    print(f"Found {len(grouped)} unique products")
    
    # Look at first product
    for pid, elements in list(grouped.items())[:3]:
        print(f"\n=== Product {pid} ===")
        for i, el in enumerate(elements):
            print(f"  Element {i}: {str(el)[:200]}")
            print(f"    Text: {el.get_text(strip=True)[:100]}")