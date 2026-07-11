import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

soup = fetch_page('https://pcparts.uk/product/22628/intel-core-i9-14900k-24-core-32-thread-up-to-6ghz-bx8071514900k')
if soup:
    # Find sections with specs
    print("=== All text containing specs ===")
    text = soup.get_text()
    # Look for key spec terms
    for term in ['core', 'thread', 'ghz', 'cache', 'socket', 'tdp', 'architecture', 'frequency']:
        import re
        matches = re.findall(rf'.{{0,50}}{term}.{{0,50}}', text, re.IGNORECASE)
        if matches:
            print(f"\n--- {term} ---")
            for m in matches[:5]:
                print(f"  {m.strip()}")
    
    # Check for spec-like divs
    print("\n=== Divs with spec-like classes ===")
    for div in soup.select("div[class*='spec'], div[class*='detail'], div[class*='attribute']"):
        print(f"  Class: {div.get('class')}")
        print(f"  Text: {div.get_text(strip=True)[:200]}")