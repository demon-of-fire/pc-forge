import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup
from collections import defaultdict

soup = fetch_page('https://pcparts.uk/browse/cpus')
if soup:
    cards = soup.select("a[href^='/product/']")
    grouped = defaultdict(list)
    for card in cards:
        pid = card.get('data-product-id')
        if pid:
            grouped[pid].append(card)
    
    # Check element counts
    counts = defaultdict(int)
    for pid, elements in grouped.items():
        counts[len(elements)] += 1
    
    print("Element count distribution:")
    for count, freq in sorted(counts.items()):
        print(f"  {count} elements: {freq} products")
    
    # Look at a product with most elements
    max_elements = max(len(e) for e in grouped.values())
    for pid, elements in grouped.items():
        if len(elements) == max_elements:
            print(f"\n=== Product {pid} with {max_elements} elements ===")
            for i, el in enumerate(elements):
                print(f"  Element {i}: {str(el)[:300]}")
            break