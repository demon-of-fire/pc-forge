"""Scrape hardware product listings and prices from PCPartPicker UK."""

import logging
import re
from datetime import datetime, timezone

from utils.scraper import fetch_page, make_slug, guess_manufacturer

logger = logging.getLogger(__name__)

BASE_URL = "https://uk.pcpartpicker.com"

CATEGORY_URLS = {
    "cpus": "/products/cpu/",
    "gpus": "/products/video-card/",
    "motherboards": "/products/motherboard/",
    "ram": "/products/memory/",
    "storage": "/products/internal-hard-drive/",
    "psus": "/products/power-supply/",
    "cases": "/products/case/",
    "coolers": "/products/cpu-cooler/",
}


def scrape_product_list(category: str, max_pages: int = 3) -> list[dict]:
    """Scrape product names and prices from PCPartPicker UK listing pages.

    Returns a list of dicts with at least: name, url, price, manufacturer.
    """
    url_path = CATEGORY_URLS.get(category)
    if not url_path:
        logger.error("Unknown category for PCPartPicker: %s", category)
        return []

    products = []
    for page_num in range(1, max_pages + 1):
        if page_num == 1:
            url = f"{BASE_URL}{url_path}"
        else:
            url = f"{BASE_URL}{url_path}page/{page_num}"

        logger.info("Fetching PCPartPicker %s page %d: %s", category, page_num, url)
        soup = fetch_page(url)
        if soup is None:
            logger.warning("Failed to fetch page %d for %s", page_num, category)
            break

        rows = soup.select("tr.tr__product")
        if not rows:
            logger.info("No more products on page %d for %s", page_num, category)
            break

        for row in rows:
            try:
                product = _parse_product_row(row, category)
                if product:
                    products.append(product)
            except Exception as e:
                logger.debug("Failed to parse row: %s", e)

        logger.info("Page %d: found %d products so far", page_num, len(products))

    logger.info("Total scraped %d products for %s", len(products), category)
    return products


def _parse_product_row(row, category: str) -> dict | None:
    """Parse a single product row from the PCPartPicker listing table."""
    name_cell = row.select_one("td.td__name")
    if not name_cell:
        return None

    link = name_cell.select_one("a")
    if not link:
        return None

    name = link.get_text(strip=True)
    href = link.get("href", "")
    product_url = f"{BASE_URL}{href}" if href.startswith("/") else href

    price_cell = row.select_one("td.td__finalPrice")
    price = None
    if price_cell:
        price_text = price_cell.get_text(strip=True)
        price = _parse_price(price_text)

    msrp_cell = row.select_one("td.td__basePrice")
    msrp = None
    if msrp_cell:
        msrp_text = msrp_cell.get_text(strip=True)
        msrp = _parse_price(msrp_text)

    manufacturer = guess_manufacturer(name)

    return {
        "name": name,
        "url": product_url,
        "price": price,
        "msrp": msrp or price,
        "manufacturer": manufacturer,
        "slug": make_slug(name),
    }


def _parse_price(text: str) -> float | None:
    """Extract numeric price from text like '£389.00' or 'From £299'."""
    if not text:
        return None
    match = re.search(r"[\d,]+\.?\d*", text.replace(",", ""))
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None


def scrape_product_detail(product_url: str) -> dict:
    """Scrape detailed specs from a PCPartPicker product detail page."""
    soup = fetch_page(product_url)
    if soup is None:
        return {}

    specs = {}
    spec_table = soup.select("table.specs tr")
    for row in spec_table:
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td:
            key = th.get_text(strip=True).lower()
            val = td.get_text(strip=True)
            specs[key] = val

    merchant_prices = []
    merchant_rows = soup.select("tr.merchant")
    for row in merchant_rows:
        name_el = row.select_one("td.merchant__name")
        price_el = row.select_one("td.merchant__finalPrice")
        link_el = row.select_one("a")
        if name_el and price_el:
            merchant_name = name_el.get_text(strip=True)
            price_val = _parse_price(price_el.get_text(strip=True))
            merchant_url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                merchant_url = f"{BASE_URL}{href}" if href.startswith("/") else href
            if price_val:
                merchant_prices.append({
                    "retailer": merchant_name,
                    "price": price_val,
                    "url": merchant_url,
                })

    return {"specs": specs, "merchant_prices": merchant_prices}


def match_to_existing(scraped: list[dict], existing: list[dict]) -> tuple[list[dict], list[dict]]:
    """Match scraped products to existing data by name similarity.

    Returns (updated_existing, new_products).
    """
    existing_by_slug = {item["slug"]: item for item in existing if "slug" in item}
    existing_by_name = {}
    for item in existing:
        name_lower = item.get("name", "").lower().strip()
        existing_by_name[name_lower] = item

    matched_slugs = set()
    new_products = []

    for prod in scraped:
        slug = prod.get("slug", "")
        name_lower = prod.get("name", "").lower().strip()

        matched_item = None
        if slug in existing_by_slug:
            matched_item = existing_by_slug[slug]
        elif name_lower in existing_by_name:
            matched_item = existing_by_name[name_lower]
        else:
            for ex_slug, ex_item in existing_by_slug.items():
                if _names_similar(name_lower, ex_item.get("name", "").lower()):
                    matched_item = ex_item
                    break

        if matched_item:
            matched_slugs.add(matched_item["slug"])
            _update_prices(matched_item, prod)
        else:
            new_products.append(prod)

    updated_existing = [item for item in existing if item.get("slug") in matched_slugs]
    unmatched_existing = [item for item in existing if item.get("slug") not in matched_slugs]
    updated_existing.extend(unmatched_existing)

    return updated_existing, new_products


def _names_similar(name1: str, name2: str) -> bool:
    """Check if two product names refer to the same product."""
    words1 = set(name1.split())
    words2 = set(name2.split())
    if not words1 or not words2:
        return False
    overlap = len(words1 & words2)
    shorter = min(len(words1), len(words2))
    return overlap / shorter > 0.7


def _update_prices(existing_item: dict, scraped: dict):
    """Update prices in existing item from scraped data."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    price = scraped.get("price")
    url = scraped.get("url", "")

    if price is None:
        return

    existing_prices = existing_item.get("prices", [])

    pcpartpicker_exists = False
    for p in existing_prices:
        if "pcpartpicker" in p.get("url", "").lower() or p.get("retailer", "").lower() == "pcpartpicker":
            p["price"] = price
            p["url"] = url
            p["lastChecked"] = now
            p["availability"] = "in-stock"
            pcpartpicker_exists = True
            break

    if not pcpartpicker_exists:
        existing_prices.append({
            "retailer": "PCPartPicker",
            "price": price,
            "currency": "GBP",
            "url": url,
            "availability": "in-stock",
            "lastChecked": now,
        })

    existing_item["prices"] = existing_prices

    if scraped.get("msrp") and existing_item.get("msrp", 0) == 0:
        existing_item["msrp"] = scraped["msrp"]
