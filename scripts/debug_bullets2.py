import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    links = soup.select("a[href^='/product/']")
    from collections import defaultdict
    grouped = defaultdict(list)
    for link in links:
        pid = link.get('data-product-id')
        if pid:
            grouped[pid].append(link)
    
    print(f"Total unique products on page 1: {len(grouped)}")
    # Show first 5 products
    for pid, elements in list(grouped.items())[:5]:
        print(f"\nProduct {pid} ({len(elements)} elements):")
        for i, el in enumerate(elements):
            text = el.get_text(strip=True)
            print(f"  Element {i}: '{text[:150]}'")