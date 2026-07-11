import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

# Test detail page extraction
from scrapers.pcpartsuk import extract_specs_from_detail_page

# CPU
soup = fetch_page('https://pcparts.uk/product/22628/intel-core-i9-14900k-24-core-32-thread-up-to-6ghz-bx8071514900k')
if soup:
    specs = extract_specs_from_detail_page('cpus', soup)
    print("=== CPU Detail Specs ===")
    for k, v in sorted(specs.items()):
        print(f"  {k}: {v}")
else:
    print("Failed to fetch CPU detail")

# Check what tables exist
if soup:
    tables = soup.select("table")
    print(f"\nFound {len(tables)} tables")
    for i, t in enumerate(tables[:5]):
        rows = t.select("tr")
        print(f"  Table {i}: {len(rows)} rows")
        for r in rows[:3]:
            th = r.select_one("th")
            td = r.select_one("td")
            if th and td:
                print(f"    {th.get_text(strip=True)}: {td.get_text(strip=True)}")

print("\n\n=== Looking for spec sections ===")
if soup:
    # Look for the spec sections
    for section in soup.select("section, .spec, .specification, [class*='spec']"):
        text = section.get_text(strip=True)
        if text and len(text) > 50:
            print(f"Section: {text[:200]}...")
            print("---")