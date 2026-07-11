import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page
from bs4 import BeautifulSoup

soup = fetch_page('https://pcparts.uk/product/22628/intel-core-i9-14900k-24-core-32-thread-up-to-6ghz-bx8071514900k')
if soup:
    # Print all tables
    tables = soup.select("table")
    print(f"Found {len(tables)} tables")
    for i, table in enumerate(tables):
        print(f"\n=== Table {i} ===")
        rows = table.select("tr")
        for row in rows:
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td:
                print(f"  {th.get_text(strip=True)}: {td.get_text(strip=True)}")
    
    # Also check for definition lists
    dls = soup.select("dl")
    print(f"\nFound {len(dls)} dl elements")
    for i, dl in enumerate(dls):
        print(f"\n=== DL {i} ===")
        dts = dl.select("dt")
        for dt in dts:
            dd = dt.find_next_sibling("dd")
            if dd:
                print(f"  {dt.get_text(strip=True)}: {dd.get_text(strip=True)}")