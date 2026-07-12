import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from scrapers.pcpartsuk import parse_card

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    cards = soup.select('div.card-horizontal')
    print(f'Cards: {len(cards)}')
    for card in cards[:2]:
        result = parse_card(card, 'psus')
        if result:
            print(f'  Name: {result["name"]}')
            print(f'  Price: {result["price"]}')
            print(f'  Specs: {result["specs"]}')
            print(f'  URL: {result["url"]}')
            print(f'  Image: {result["image"]}')
            print()