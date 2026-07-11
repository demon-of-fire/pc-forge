import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

soup = fetch_page('https://pcparts.uk/browse/cpus')
if soup:
    # Find a product card
    cards = soup.select("a[href^='/product/']")
    print(f"Found {len(cards)} product links")
    
    # Let's look at the first few
    for i, card in enumerate(cards[:3]):
        print(f"\n=== Card {i} ===")
        print(f"HTML: {str(card)[:500]}")
        print(f"Text: {card.get_text(strip=True)[:200]}")
        
        # Check for image
        img = card.select_one("img")
        if img:
            print(f"Img alt: {img.get('alt')}")
            print(f"Img src: {img.get('src')}")