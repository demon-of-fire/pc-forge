"""Scrape hardware product listings and prices from pcparts.uk."""

import logging
import re
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict

from bs4 import BeautifulSoup

from utils.scraper import fetch_page, make_slug, guess_manufacturer

logger = logging.getLogger(__name__)

BASE_URL = "https://pcparts.uk"

CATEGORY_URLS = {
    "cpus": "/browse/cpus",
    "gpus": "/browse/graphics-cards",
    "motherboards": "/browse/motherboards",
    "ram": "/browse/memory",
    "storage": "/browse/solid-state-drives",
    "psus": "/browse/power-supplies",
    "cases": "/browse/cases",
    "coolers": "/browse/cpu-coolers",
}


def parse_price(text: str) -> Optional[float]:
    """Extract price from text like '£439.99' or 'out of stock'."""
    if not text:
        return None
    text = text.lower().strip()
    if "out of stock" in text:
        return None
    match = re.search(r"[\d,]+\.?\d*", text.replace(",", ""))
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None


def extract_specs_from_name(category: str, name: str) -> dict:
    """Extract basic specs from product name as fallback."""
    specs = {}
    lower = name.lower()

    if category == "cpus":
        core_match = re.search(r"(\d+)\s*[-\s]?core", lower)
        if core_match:
            specs["cores"] = int(core_match.group(1))
        thread_match = re.search(r"(\d+)\s*[-\s]?thread", lower)
        if thread_match:
            specs["threads"] = int(thread_match.group(1))
        base_match = re.search(r"(\d+\.?\d*)\s*ghz\s*base", lower)
        if base_match:
            specs["base_clock"] = float(base_match.group(1))
        boost_match = re.search(r"(\d+\.?\d*)\s*ghz\s*boost", lower) or \
                      re.search(r"up to\s*(\d+\.?\d*)\s*ghz", lower)
        if boost_match:
            specs["boost_clock"] = float(boost_match.group(1))
        socket_match = re.search(r"(lga\d+|am\d+)", lower)
        if socket_match:
            specs["socket"] = socket_match.group(1).upper()

    elif category == "gpus":
        vram_match = re.search(r"(\d+)\s*gb", lower)
        if vram_match:
            specs["vram_gb"] = int(vram_match.group(1))
        if "gddr7" in lower:
            specs["memory_type"] = "GDDR7"
        elif "gddr6x" in lower:
            specs["memory_type"] = "GDDR6X"
        elif "gddr6" in lower:
            specs["memory_type"] = "GDDR6"
        elif "gddr5" in lower:
            specs["memory_type"] = "GDDR5"
        elif "hbm" in lower:
            specs["memory_type"] = "HBM"
        if "rtx" in lower:
            specs["chipset"] = re.search(r"(rtx\s+\d+)", lower).group(1).upper() if re.search(r"(rtx\s+\d+)", lower) else "RTX"
        elif "gtx" in lower:
            specs["chipset"] = re.search(r"(gtx\s+\d+)", lower).group(1).upper() if re.search(r"(gtx\s+\d+)", lower) else "GTX"
        elif "rx" in lower:
            specs["chipset"] = re.search(r"(rx\s+\d+)", lower).group(1).upper() if re.search(r"(rx\s+\d+)", lower) else "RX"

    elif category == "ram":
        cap_match = re.search(r"(\d+)\s*gb\s*(?:\(\s*(\d+)\s*x\s*(\d+)\s*gb\s*\))?", lower) or \
                    re.search(r"(\d+)\s*x\s*(\d+)\s*gb", lower)
        if cap_match:
            if len(cap_match.groups()) == 3:
                specs["capacity_gb"] = int(cap_match.group(1))
                specs["modules"] = int(cap_match.group(2))
                specs["module_size_gb"] = int(cap_match.group(3))
            else:
                specs["modules"] = int(cap_match.group(1))
                specs["module_size_gb"] = int(cap_match.group(2))
                specs["capacity_gb"] = int(cap_match.group(1)) * int(cap_match.group(2))
        if "ddr5" in lower:
            specs["type"] = "DDR5"
        elif "ddr4" in lower:
            specs["type"] = "DDR4"
        speed_match = re.search(r"(\d+)\s*(?:mhz|mt/s)", lower)
        if speed_match:
            specs["speed_mhz"] = int(speed_match.group(1))
        cas_match = re.search(r"(?:cl|cas)[\s-]?(\d+)", lower)
        if cas_match:
            specs["cas_latency"] = int(cas_match.group(1))

    elif category == "storage":
        cap_match = re.search(r"(\d+)\s*(?:tb|gb)", lower)
        if cap_match:
            val = int(cap_match.group(1))
            specs["capacity_gb"] = val * 1000 if "tb" in cap_match.group(0) else val
        if "m.2" in lower or "m2" in lower:
            specs["form_factor"] = "M.2"
        elif "2.5" in lower:
            specs["form_factor"] = "2.5\""
        if "pcie 5" in lower or "pci-e 5" in lower:
            specs["interface"] = "PCIe 5.0"
        elif "pcie 4" in lower or "pci-e 4" in lower:
            specs["interface"] = "PCIe 4.0"
        elif "nvme" in lower:
            specs["interface"] = "NVMe"
        elif "sata" in lower:
            specs["interface"] = "SATA"

    elif category == "psus":
        w_match = re.search(r"(\d+)\s*w", lower)
        if w_match:
            specs["wattage"] = int(w_match.group(1))
        if "titanium" in lower:
            specs["efficiency"] = "80+ Titanium"
        elif "platinum" in lower:
            specs["efficiency"] = "80+ Platinum"
        elif "gold" in lower:
            specs["efficiency"] = "80+ Gold"
        elif "silver" in lower:
            specs["efficiency"] = "80+ Silver"
        elif "bronze" in lower:
            specs["efficiency"] = "80+ Bronze"
        if "fully" in lower and "modular" in lower:
            specs["modular"] = "Full"
        elif "semi" in lower and "modular" in lower:
            specs["modular"] = "Semi"
        elif "non" in lower and "modular" in lower:
            specs["modular"] = "None"
        if "sfx" in lower:
            specs["form_factor"] = "SFX"
        elif "tfx" in lower:
            specs["form_factor"] = "TFX"
        else:
            specs["form_factor"] = "ATX"

    elif category == "coolers":
        if "liquid" in lower or "water" in lower or "aio" in lower:
            specs["type"] = "Liquid"
        else:
            specs["type"] = "Air"
        rad_match = re.search(r"(\d+)\s*mm", lower)
        if rad_match:
            specs["radiator_mm"] = int(rad_match.group(1))
        if "dual" in lower and "fan" in lower:
            specs["fan_count"] = 2
        elif "triple" in lower and "fan" in lower:
            specs["fan_count"] = 3
        elif "single" in lower and "fan" in lower:
            specs["fan_count"] = 1

    elif category == "cases":
        if "full" in lower and "tower" in lower:
            specs["form_factor"] = "Full Tower"
        elif "mid" in lower and "tower" in lower:
            specs["form_factor"] = "Mid Tower"
        elif "mini" in lower and "tower" in lower:
            specs["form_factor"] = "Mini Tower"
        elif "micro" in lower and "tower" in lower:
            specs["form_factor"] = "Micro Tower"
        elif "itx" in lower or "mini-itx" in lower:
            specs["form_factor"] = "Mini-ITX"
        elif "sff" in lower or "small form" in lower:
            specs["form_factor"] = "SFF"
        gpu_match = re.search(r"gpu.*?(\d+)\s*mm", lower)
        if gpu_match:
            specs["max_gpu_length_mm"] = int(gpu_match.group(1))
        cooler_match = re.search(r"cooler.*?(\d+)\s*mm", lower)
        if cooler_match:
            specs["max_cooler_height_mm"] = int(cooler_match.group(1))
        if "tempered" in lower and "glass" in lower:
            specs["side_panel"] = "Tempered Glass"
        elif "mesh" in lower:
            specs["side_panel"] = "Mesh"

    return specs


def extract_specs_from_detail_page(category: str, soup: BeautifulSoup) -> dict:
    """Extract detailed specs from a product detail page."""
    specs = {}

    # Parse spec-item elements (label + value pairs)
    for item in soup.select(".spec-item, .specification-item, .spec-row"):
        label_el = item.select_one(".spec-label, .spec-name, .label, dt, .name")
        value_el = item.select_one(".spec-value, .spec-data, .value, dd, .data")

        if label_el and value_el:
            key = label_el.get_text(strip=True).lower()
            val = value_el.get_text(strip=True)
            if key and val:
                specs[key] = val
        else:
            # Try to split text by looking for known label patterns
            text = item.get_text(strip=True)
            if text:
                for pattern in [r"^(.+?)\s*[:\-]\s*(.+)$", r"^(.+?)\s{2,}(.+)$"]:
                    match = re.match(pattern, text)
                    if match:
                        key = match.group(1).strip().lower()
                        val = match.group(2).strip()
                        if key and val:
                            specs[key] = val
                        break

    # Parse table rows with th/td
    for table in soup.select("table.specs, table.specifications, table.spec-table, table"):
        for row in table.select("tr"):
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td:
                key = th.get_text(strip=True).lower()
                val = td.get_text(strip=True)
                if key and val:
                    specs[key] = val

    # Parse dl/dt/dd structures
    for dt in soup.select("dt"):
        dd = dt.find_next_sibling("dd")
        if dd:
            key = dt.get_text(strip=True).lower()
            val = dd.get_text(strip=True)
            if key and val:
                specs[key] = val

    # Parse section text for concatenated label-value pairs
    section_text = ""
    for section in soup.select("section, .spec-section, .specification-section"):
        section_text += " " + section.get_text(strip=True)

    if section_text:
        patterns = {
            "cpus": [
                (r"total cores\s*(\d+)", "cores"),
                (r"total threads\s*(\d+)", "threads"),
                (r"max turbo frequency\s*([\d.]+)\s*ghz", "boost_clock"),
                (r"base frequency\s*([\d.]+)\s*ghz", "base_clock"),
                (r"processor base frequency\s*([\d.]+)\s*ghz", "base_clock"),
                (r"processor max turbo frequency\s*([\d.]+)\s*ghz", "boost_clock"),
                (r"cache\s*(\d+)\s*mb", "cache"),
                (r"l3 cache\s*(\d+)\s*mb", "cache"),
                (r"socket\s*(lga\d+|am\d+)", "socket"),
                (r"tdp\s*(\d+)\s*w", "tdp"),
                (r"default tdp\s*(\d+)\s*w", "tdp"),
                (r"microarchitecture\s*([a-z0-9\s]+)", "architecture"),
                (r"core name\s*([a-z0-9\s]+)", "architecture"),
            ],
            "gpus": [
                (r"memory\s*(\d+)\s*gb", "vram"),
                (r"memory type\s*(gddr\d+x?|hbm\d+)", "memory_type"),
                (r"core clock\s*(\d+)\s*mhz", "core_clock"),
                (r"boost clock\s*(\d+)\s*mhz", "boost_clock"),
                (r"memory clock\s*(\d+)\s*mhz", "memory_clock"),
                (r"tdp\s*(\d+)\s*w", "tdp"),
                (r"power consumption\s*(\d+)\s*w", "tdp"),
                (r"length\s*(\d+)\s*mm", "length_mm"),
            ],
            "motherboards": [
                (r"form factor\s*(e-atx|atx|micro-atx|mini-itx|eatx|matx|mitx)", "form_factor"),
                (r"chipset\s*(b\d{3}|x\d{3}|z\d{3}|h\d{3}|a\d{3})", "chipset"),
                (r"cpu socket\s*(lga\d+|am\d+)", "socket"),
                (r"memory type\s*(ddr\d+)", "memory_type"),
                (r"memory slots\s*(\d+)", "memory_slots"),
                (r"m\.?2 slots\s*(\d+)", "m2_slots"),
            ],
            "ram": [
                (r"capacity\s*(\d+)\s*gb", "capacity"),
                (r"module capacity\s*(\d+)\s*gb", "module_size"),
                (r"number of modules\s*(\d+)", "modules"),
                (r"speed\s*(\d+)\s*(?:mhz|mt/s)", "speed"),
                (r"cas latency\s*(\d+)", "cas_latency"),
                (r"voltage\s*([\d.]+)\s*v", "voltage"),
            ],
            "storage": [
                (r"capacity\s*(\d+)\s*(tb|gb)", "capacity"),
                (r"form factor\s*(m\.?2|2\.5\")", "form_factor"),
                (r"interface\s*(pcie\s*\d\.?\d*|nvme|sata)", "interface"),
                (r"max sequential read\s*(\d+)\s*mb", "max_read"),
                (r"max sequential write\s*(\d+)\s*mb", "max_write"),
            ],
            "psus": [
                (r"wattage\s*(\d+)\s*w", "wattage"),
                (r"efficiency\s*(80\+\s*(titanium|platinum|gold|silver|bronze))", "efficiency"),
                (r"modular\s*(full|semi|none)", "modular"),
                (r"form factor\s*(atx|sfx|tfx)", "form_factor"),
            ],
            "coolers": [
                (r"type\s*(liquid|water|aio|air)", "cooler_type"),
                (r"radiator size\s*(\d+)\s*mm", "radiator_mm"),
                (r"fan count\s*(\d+)", "fan_count"),
            ],
            "cases": [
                (r"form factor\s*(full tower|mid tower|mini tower|micro tower|mini-itx|sff)", "form_factor"),
                (r"max gpu length\s*(\d+)\s*mm", "max_gpu_length"),
                (r"max cpu cooler height\s*(\d+)\s*mm", "max_cooler_height"),
                (r"side panel\s*(tempered glass|mesh)", "side_panel"),
            ],
        }
        
        cat_patterns = patterns.get(category, [])
        lower_text = section_text.lower()
        for pattern, key in cat_patterns:
            match = re.search(pattern, lower_text)
            if match:
                if key in ["cores", "threads", "vram", "modules", "memory_slots", "m2_slots", "fan_count", "max_gpu_length", "max_cooler_height", "capacity"]:
                    specs[key] = int(match.group(1))
                elif key in ["boost_clock", "base_clock", "speed", "core_clock", "boost_clock", "memory_clock"]:
                    specs[key] = float(match.group(1))
                elif key in ["cache", "wattage", "tdp", "length_mm", "radiator_mm", "max_gpu_length", "max_cooler_height", "max_gpu_length", "max_cooler_height"]:
                    specs[key] = int(match.group(1))
                elif key in ["socket", "architecture", "chipset", "memory_type", "form_factor", "interface", "modular", "cooler_type", "side_panel"]:
                    specs[key] = match.group(1).upper() if key in ["socket", "chipset"] else match.group(1).title()
                else:
                    specs[key] = match.group(1)

    # Map extracted keys to normalized format
    key_map = {
        # CPUs
        "total cores": "cores",
        "total threads": "threads",
        "max turbo frequency": "boost_clock",
        "base frequency": "base_clock",
        "processor base frequency": "base_clock",
        "processor max turbo frequency": "boost_clock",
        "cache": "cache",
        "l3 cache": "cache",
        "socket": "socket",
        "tdp": "tdp",
        "default tdp": "tdp",
        "microarchitecture": "architecture",
        "core name": "architecture",

        # GPUs
        "memory": "vram",
        "memory size": "vram",
        "memory type": "memory_type",
        "core clock": "core_clock",
        "boost clock": "boost_clock",
        "memory clock": "memory_clock",
        "tdp": "tdp",
        "power consumption": "tdp",
        "length": "length_mm",

        # Motherboards
        "form factor": "form_factor",
        "chipset": "chipset",
        "cpu socket": "socket",
        "memory type": "memory_type",
        "memory slots": "memory_slots",
        "m.2 slots": "m2_slots",

        # RAM
        "capacity": "capacity",
        "module capacity": "module_size",
        "number of modules": "modules",
        "speed": "speed",
        "cas latency": "cas_latency",
        "voltage": "voltage",

        # Storage
        "capacity": "capacity",
        "form factor": "form_factor",
        "interface": "interface",
        "max sequential read": "max_read",
        "max sequential write": "max_write",

        # PSUs
        "wattage": "wattage",
        "efficiency": "efficiency",
        "modular": "modular",
        "form factor": "form_factor",

        # Coolers
        "type": "cooler_type",
        "radiator size": "radiator_mm",
        "fan count": "fan_count",

        # Cases
        "form factor": "form_factor",
        "max gpu length": "max_gpu_length",
        "max cpu cooler height": "max_cooler_height",
        "side panel": "side_panel",
    }

    normalized = {}
    for key, val in specs.items():
        key_lower = key.lower().strip()
        if key_lower in key_map:
            normalized[key_map[key_lower]] = val
        else:
            normalized[key_lower] = val

    return normalized


def parse_card(card: BeautifulSoup, category: str, fetch_details: bool = False) -> Optional[dict]:
    """Parse a product card from the listing page."""
    # Find the product link
    link = card.select_one("a[href^='/product/']")
    if not link:
        return None

    pid = link.get("data-product-id", "")
    
    # Get name from image alt or card text
    name = ""
    img = card.select_one("img")
    if img and img.get("alt"):
        name = img.get("alt", "").strip()
    else:
        # Extract name from card text (before price)
        text = card.get_text(strip=True)
        name = text.split("£")[0].strip()[:150]

    if not name:
        return None

    # Extract price
    price_text = card.get_text(strip=True)
    price_match = re.search(r"£([\d,]+\.?\d*)", price_text)
    price = None
    if price_match:
        price = float(price_match.group(1).replace(",", ""))

    # Extract specs from <li> elements in the card
    specs = {}
    for li in card.select("ul li"):
        text = li.get_text(strip=True)
        if not text:
            continue
        # Parse "Key: Value" or "Value Unit"
        if ":" in text:
            key, val = text.split(":", 1)
            specs[key.strip()] = val.strip()
        else:
            # Parse "750W", "80+ Gold", "ATX Form Factor", "Fully-Modular"
            match = re.match(r"^(.+?)\s+([\d,]+\.?\d*)\s*(\w*)$", text)
            if match:
                label = match.group(1).strip()
                val = match.group(2).replace(",", "")
                unit = match.group(3)
                if unit:
                    specs[label] = f"{val} {unit}"
                else:
                    specs[label] = val
            else:
                # Simple text specs like "80+ Gold", "ATX Form Factor", "Fully-Modular"
                lower = text.lower()
                if any(x in lower for x in ["gold", "platinum", "silver", "bronze", "titanium", "cybenetics"]):
                    specs["efficiency"] = text
                elif "modular" in lower:
                    specs["modular"] = text
                elif "form factor" in lower or "atx" in lower or "sfx" in lower or "tfx" in lower:
                    specs["form_factor"] = text
                elif "cooling" in lower:
                    specs["cooling"] = text
                elif "w" in lower and re.search(r"\d+w", lower):
                    # Extract wattage number
                    w_match = re.search(r"(\d+)\s*w", lower)
                    if w_match:
                        specs["wattage"] = int(w_match.group(1))
                    else:
                        specs["wattage_text"] = text
                else:
                    specs["feature"] = text

    # Get URL
    href = card.select_one("a[href^='/product/']")
    product_url = ""
    if href and href.get("href"):
        href_val = href.get("href", "")
        product_url = f"{BASE_URL}{href_val}" if href_val.startswith("/") else href_val

    # Extract image
    image = ""
    img_el = card.select_one("img")
    if img_el:
        src = img_el.get("src", "") or img_el.get("data-src", "")
        if src and src.startswith("/"):
            image = f"{BASE_URL}{src}"

    # Extract specs from name as fallback
    name_specs = extract_specs_from_name(category, name)
    # Merge listing specs (they take priority)
    name_specs.update(specs)
    specs = name_specs

    # Optionally fetch detail page for full specs
    product_url = ""
    href = card.select_one("a[href^='/product/']")
    if href and href.get("href"):
        href_val = href.get("href", "")
        product_url = f"{BASE_URL}{href_val}" if href_val.startswith("/") else href_val

    if fetch_details and product_url:
        try:
            detail_soup = fetch_page(product_url)
            if detail_soup:
                detail_specs = extract_specs_from_detail_page(category, detail_soup)
                specs.update(detail_specs)
        except Exception as e:
            logger.debug("Failed to fetch detail page for %s: %s", name, e)

    return {
        "name": name,
        "url": product_url,
        "price": price,
        "manufacturer": guess_manufacturer(name),
        "slug": make_slug(name),
        "specs": specs,
        "image": image,
        "source": "pcparts.uk",
        "external_id": card.select_one("a[data-product-id]").get("data-product-id", "") if card.select_one("a[data-product-id]") else "",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def scrape_category(category: str, max_pages: int = 5, fetch_details: bool = False, max_details: int = 10) -> list[dict]:
    """Scrape a category from pcparts.uk."""
    if category not in CATEGORY_URLS:
        logger.error("Unknown category: %s", category)
        return []

    products = []
    base_path = CATEGORY_URLS[category]
    details_fetched = 0

    for page_num in range(1, max_pages + 1):
        if page_num == 1:
            url = f"{BASE_URL}{base_path}"
        else:
            url = f"{BASE_URL}{base_path}?page={page_num}"

        logger.info("Fetching %s page %d: %s", category, page_num, url)
        soup = fetch_page(url)
        if not soup:
            logger.warning("Failed to fetch page %d for %s", page_num, category)
            break

        # Find all card-horizontal containers
        cards = soup.select("div.card-horizontal")
        if not cards:
            logger.info("No more products on page %d for %s", page_num, category)
            break

        page_products = 0
        for card in cards:
            try:
                fetch_this_detail = fetch_details and details_fetched < max_details
                product = parse_card(card, category, fetch_this_detail)
                if fetch_this_detail:
                    details_fetched += 1
                if product:
                    products.append(product)
                    page_products += 1
            except Exception as e:
                logger.debug("Failed to parse card: %s", e)

        logger.info("Page %d: parsed %d products", page_num, page_products)

        if page_products == 0:
            break

    logger.info("Total scraped for %s: %d products (details for %d)", category, len(products), details_fetched)
    return products


def scrape_all_categories(max_pages_per_category: int = 5) -> dict[str, list[dict]]:
    """Scrape all categories from pcparts.uk."""
    results = {}
    for category in CATEGORY_URLS.keys():
        logger.info("=== Scraping %s ===", category)
        try:
            results[category] = scrape_category(category, max_pages=max_pages_per_category)
        except Exception as e:
            logger.error("Failed to scrape %s: %s", category, e)
            results[category] = []
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    data = scrape_all_categories(max_pages_per_category=2)
    for cat, products in data.items():
        print(f"{cat}: {len(products)} products")
        for p in products[:3]:
            print(f"  - {p['name']} @ £{p['price']}")