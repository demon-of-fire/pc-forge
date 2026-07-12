import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    # Find the card-horizontal containers
    cards = soup.select("div.card-horizontal")
    print(f"Found {len(cards)} card-horizontal containers")
    
    for card in cards[:2]:
        print(f"\n=== Card ===")
        # Find all text content
        for child in card.find_all(['li', 'div', 'span', 'ul'], recursive=True):
            text = child.get_text(strip=True)
            if text and len(text) > 5 and not text.startswith('P C P A R T S U K'):
                # Skip nav text
                if not any(x in text.lower() for x in ['theme', 'cases', 'cpus', 'graphics', 'memory', 'motherboards', 'power supplies', 'press enter', 'search', 'categories', 'brands']):
                    print(f"  {child.name}: {text[:200]}")