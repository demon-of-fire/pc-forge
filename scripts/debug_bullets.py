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
    
    # Find Deepcool PM650D
    for pid, elements in grouped.items():
        if pid == '15972':
            print(f"Product {pid} has {len(elements)} elements")
            for i, el in enumerate(elements):
                text = el.get_text(strip=True)
                print(f"  Element {i}: '{text[:150]}'")
            break