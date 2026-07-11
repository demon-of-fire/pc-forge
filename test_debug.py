import sys
sys.path.insert(0, 'scripts')
from utils.scraper import fetch_page

url = "https://pcparts.uk/browse/cpus"
soup = fetch_page(url)
if soup:
    rows = soup.select("tr.tr__product")
    print(f"Found {len(rows)} rows with tr.tr__product")
    
    # Try other selectors
    products = soup.select("[data-product-id]")
    print(f"Found {len(products)} with [data-product-id]")
    
    # Check for product links
    links = soup.select("a[href*='/product/']")
    print(f"Found {len(links)} product links")
    
    # Print first few product cards
    cards = soup.select(".product-card, .product-item, article, .grid > div")
    print(f"Found {len(cards)} potential product cards")
    
    # Look at the structure
    for i, card in enumerate(cards[:3]):
        print(f"\nCard {i}:")
        print(card.prettify()[:500])
else:
    print("Failed to fetch page")