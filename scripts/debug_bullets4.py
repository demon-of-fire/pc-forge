import sys
sys.path.insert(0, 'scripts')

from utils.scraper import fetch_page

soup = fetch_page('https://pcparts.uk/browse/power-supplies')
if soup:
    # Find a product link and traverse up to the product container
    links = soup.select("a[href^='/product/']")
    link = links[0]
    pid = link.get('data-product-id')
    print(f"Product ID: {pid}")
    
    # Go up to find the full product card
    current = link
    for _ in range(5):
        current = current.parent
        if current and current.name:
            print(f"  {current.name} class={current.get('class')}")
            if 'product' in str(current.get('class', [])) or 'result' in str(current.get('class', [])):
                print(f"  Found product container!")
                print(current.prettify()[:3000])
                break