import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    # Find the product container
    links = soup.select("a[href^='/product/']")
    from collections import defaultdict
    grouped = defaultdict(list)
    for link in links:
        pid = link.get('data-product-id')
        if pid:
            grouped[pid].append(link)
    
    # Find a product and check its parent
    for pid, elements in list(grouped.items())[:3]:
        print(f"\nProduct {pid}:")
        parent = elements[0].parent
        print(f"  Parent: {parent.name} class={parent.get('class')}")
        # Find all siblings/children
        for sibling in parent.find_all(['li', 'ul', 'div', 'span'], recursive=False):
            text = sibling.get_text(strip=True)
            if text and len(text) > 5:
                print(f"  Child: {text[:100]}")