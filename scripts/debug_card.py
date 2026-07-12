import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
import re

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    cards = soup.select('div.card-horizontal')
    print(f'Cards: {len(cards)}')
    for card in cards[:2]:
        # Check for product link
        link = card.select_one("a[href^='/product/']")
        print(f'  Link: {link}')
        if link:
            print(f'  PID: {link.get("data-product-id")}')
        
        # Check for price
        price_match = re.search(r'£([\d,]+\.?\d*)', card.get_text(strip=True))
        print(f'  Price: {price_match}')
        
        # Check for specs in ul li
        for li in card.select('ul li'):
            print(f'  LI: {li.get_text(strip=True)}')