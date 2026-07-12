#!/usr/bin/env python3
"""Normalize all existing data files to ensure required fields."""

import json
import logging
from pathlib import Path

from scrapers.pcpartpicker import _normalize_scraped_product, guess_manufacturer, make_slug

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data"

CATEGORIES = [
    "cpus", "gpus", "motherboards", "ram",
    "storage", "psus", "cases", "coolers"
]

# Category to type mapping
TYPE_MAP = {
    "cpus": "cpu",
    "gpus": "gpu",
    "motherboards": "motherboard",
    "ram": "ram",
    "storage": "storage",
    "psus": "psu",
    "cases": "case",
    "coolers": "cooler",
}

# Spec key mapping from scraped format to our format
SPEC_KEY_MAP = {
    "total cores": "cores",
    "total threads": "threads",
    "max turbo frequency": "boost_clock_ghz",
    "base frequency": "base_clock_ghz",
    "l2 cache": "cache",
    "l3 cache": "cache",
    "smart cache": "cache",
    "socket": "socket",
    "tdp": "tdp_w",
    "default tdp": "tdp_w",
    "memory": "vram_gb",
    "memory size": "vram_gb",
    "memory type": "memory_type",
    "core clock": "core_clock_mhz",
    "boost clock": "boost_clock_mhz",
    "memory clock": "memory_clock_mhz",
    "power consumption": "tdp_w",
    "length": "length_mm",
    "form factor": "form_factor",
    "chipset": "chipset",
    "cpu socket": "socket",
    "memory slots": "memory_slots",
    "m.2 slots": "m2_slots",
    "capacity": "capacity_gb",
    "module capacity": "module_size_gb",
    "number of modules": "modules",
    "speed": "speed_mhz",
    "cas latency": "cas_latency",
    "voltage": "voltage",
    "interface": "interface",
    "max sequential read": "max_read_mbps",
    "max sequential write": "max_write_mbps",
    "wattage": "wattage",
    "efficiency": "efficiency",
    "modular": "modularity",
    "max gpu length": "max_gpu_length_mm",
    "max cpu cooler height": "max_cooler_height_mm",
    "side panel": "side_panel",
    "type": "cooler_type",
    "radiator size": "radiator_mm",
    "fan count": "fan_count",
    
    # pcparts.uk specific keys
    "total power": "wattage",
    "efficiency rating": "efficiency",
    "modularity": "modularity",
    "cooling": "cooling",
    "cooling fan diameter": "fan_size_mm",
    "pcie 16-pin / 12+4-pin quantity": "pcie_16pin_qty",
    "pcie 8-pin / 6+2-pin quantity": "pcie_8pin_qty",
    "pcie 6-pin quantity": "pcie_6pin_qty",
    "sata power quantity": "sata_qty",
    "molex 4-pin connectors": "molex_qty",
    "max output current (+12v total)": "max_12v_a",
    "power protection": "protection",
    "colour": "color",
    "length (front to back)": "length_mm",
    "width (side to side)": "width_mm",
    "height": "height_mm",
    "manufacturer codes": "manufacturer_codes",
    "barcodes": "barcodes",
}


def normalize_specs(specs: dict, category: str) -> dict:
    """Normalize spec keys to standard format."""
    normalized = {}
    for key, value in specs.items():
        lower_key = key.lower().strip()
        if lower_key in SPEC_KEY_MAP:
            normalized[SPEC_KEY_MAP[lower_key]] = value
        else:
            normalized[lower_key] = value
    return normalized


def ensure_required_fields(item: dict, category: str) -> dict:
    """Ensure all required fields are present with sensible defaults."""
    if "id" not in item:
        slug = item.get("slug") or make_slug(item.get("name", "unknown"))
        item["id"] = f"{TYPE_MAP.get(category, 'cpu')}-{slug}"

    if "slug" not in item:
        item["slug"] = make_slug(item.get("name", "unknown"))

    if "name" not in item:
        item["name"] = "Unknown"

    if "manufacturer" not in item:
        item["manufacturer"] = guess_manufacturer(item.get("name", ""))

    if "image" not in item:
        item["image"] = ""

    if "releaseDate" not in item:
        item["releaseDate"] = "2023-01-01"

    if "msrp" not in item:
        item["msrp"] = 0

    if "description" not in item:
        item["description"] = f"{item.get('name', 'Unknown')} - high-performance PC component."

    if "prices" not in item:
        item["prices"] = []

    if "type" not in item:
        item["type"] = TYPE_MAP.get(category, "cpu")

    if "specs" not in item:
        item["specs"] = {}

    # Promote key specs to top-level fields
    specs = item.get("specs", {})
    if category == "cpus":
        item.setdefault("cores", specs.get("cores", 0))
        item.setdefault("threads", specs.get("threads", 0))
        item.setdefault("baseFrequency", specs.get("base_clock_ghz", 0))
        item.setdefault("boostFrequency", specs.get("boost_clock_ghz", 0))
        item.setdefault("cache", specs.get("cache", "N/A"))
        item.setdefault("socket", specs.get("socket", "N/A"))
        item.setdefault("tdp", specs.get("tdp_w", 0))
    elif category == "gpus":
        item.setdefault("vram", specs.get("vram_gb", 0))
        item.setdefault("memoryType", specs.get("memory_type", "N/A"))
        item.setdefault("coreClock", specs.get("core_clock_mhz", 0))
        item.setdefault("boostClock", specs.get("boost_clock_mhz", 0))
        item.setdefault("tdp", specs.get("tdp_w", 0))
        item.setdefault("length", specs.get("length_mm", 0))
    elif category == "motherboards":
        item.setdefault("socket", specs.get("socket", "N/A"))
        item.setdefault("chipset", specs.get("chipset", "N/A"))
        item.setdefault("formFactor", specs.get("form_factor", "N/A"))
        item.setdefault("memoryType", specs.get("memory_type", "N/A"))
        item.setdefault("memorySlots", specs.get("memory_slots", 0))
        item.setdefault("m2Slots", specs.get("m2_slots", 0))
    elif category == "ram":
        item.setdefault("capacity", specs.get("capacity_gb", 0))
        item.setdefault("memoryType", specs.get("type", "N/A"))
        item.setdefault("speed", specs.get("speed_mhz", 0))
        item.setdefault("casLatency", specs.get("cas_latency", 0))
        item.setdefault("modules", specs.get("modules", 0))
        item.setdefault("voltage", specs.get("voltage", "N/A"))
    elif category == "storage":
        item.setdefault("capacity", specs.get("capacity_gb", 0))
        item.setdefault("formFactor", specs.get("form_factor", "N/A"))
        item.setdefault("interface", specs.get("interface", "N/A"))
        item.setdefault("maxRead", specs.get("max_read_mbps", 0))
        item.setdefault("maxWrite", specs.get("max_write_mbps", 0))
    elif category == "psus":
        item.setdefault("wattage", specs.get("wattage", 0))
        item.setdefault("efficiency", specs.get("efficiency", "N/A"))
        item.setdefault("modularity", specs.get("modularity", "N/A"))
        item.setdefault("formFactor", specs.get("form_factor", "N/A"))
    elif category == "cases":
        item.setdefault("formFactor", specs.get("form_factor", "N/A"))
        item.setdefault("maxGpuLength", specs.get("max_gpu_length_mm", 0))
        item.setdefault("maxCpuCoolerHeight", specs.get("max_cooler_height_mm", 0))
        item.setdefault("sidePanel", specs.get("side_panel", "N/A"))
    elif category == "coolers":
        item.setdefault("coolerType", specs.get("cooler_type", "N/A"))
        item.setdefault("radiatorSize", specs.get("radiator_mm", 0))
        item.setdefault("fanCount", specs.get("fan_count", 0))
        item.setdefault("socket", specs.get("socket", "N/A"))

    return item


def normalize_file(category: str):
    """Normalize a single data file."""
    path = DATA_DIR / f"{category}.json"
    if not path.exists():
        logger.warning("File not found: %s", path)
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info("Normalizing %d items in %s...", len(data), category)
    normalized = []

    for item in data:
        # Normalize specs
        if "specs" in item:
            item["specs"] = normalize_specs(item["specs"], category)

        # Ensure required fields
        item = ensure_required_fields(item, category)

        normalized.append(item)

    # Save back
    with open(path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    logger.info("Normalized and saved %d items to %s", len(normalized), path)


def main():
    for cat in CATEGORIES:
        normalize_file(cat)


if __name__ == "__main__":
    main()