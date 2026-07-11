import logging
from datetime import datetime, timezone
from pathlib import Path

from .base_processor import BaseProcessor, DATA_DIR
from scrapers.pcpartpicker import scrape_product_list, match_to_existing

logger = logging.getLogger(__name__)


class RAMProcessor(BaseProcessor):
    CATEGORY = "ram"

    def fetch_data(self) -> list[dict]:
        scraped = scrape_product_list("ram", max_pages=3)
        existing = self._load_existing(DATA_DIR / "ram.json")
        if scraped and existing:
            updated, new_prods = match_to_existing(scraped, existing)
            logger.info("Matched %d existing, found %d new RAM kits", len(updated), len(new_prods))
            return updated
        return scraped

    def seed_data(self) -> list[dict]:
        return [
            {"id": "ram-corsair-veng-6000", "slug": "corsair-vengeance-ddr5-6000-32gb", "name": "Corsair Vengeance DDR5 32GB (2x16GB) 6000MHz", "manufacturer": "Corsair", "image": "/images/ram/vengeance-6000.jpg", "officialUrl": "https://www.corsair.com/...", "releaseDate": "2022-10-01", "msrp": 129, "description": "High-performance DDR5 memory for modern gaming systems.", "prices": [{"retailer": "Amazon", "price": 109, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "ram", "capacity": 32, "speed": 6000, "ddrGeneration": "DDR5", "casLatency": 36, "kitSize": 2, "modules": "2x16GB", "voltage": 1.35, "heatspreader": True, "rgb": False},
            {"id": "ram-gskill-trident-6400", "slug": "gskill-trident-z5-ddr5-6400-32gb", "name": "G.Skill Trident Z5 RGB DDR5 32GB (2x16GB) 6400MHz", "manufacturer": "G.Skill", "image": "/images/ram/trident-6400.jpg", "officialUrl": "https://www.gskill.com/...", "releaseDate": "2023-01-01", "msrp": 149, "description": "Premium overclocked memory with stunning RGB lighting.", "prices": [{"retailer": "Scan", "price": 135, "currency": "GBP", "url": "https://scan.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "ram", "capacity": 32, "speed": 6400, "ddrGeneration": "DDR5", "casLatency": 32, "kitSize": 2, "modules": "2x16GB", "voltage": 1.4, "heatspreader": True, "rgb": True},
            {"id": "ram-kingston-fury-3200", "slug": "kingston-fury-beast-ddr4-3200-16gb", "name": "Kingston FURY Beast DDR4 16GB (2x8GB) 3200MHz", "manufacturer": "Kingston", "image": "/images/ram/fury-3200.jpg", "officialUrl": "https://www.kingston.com/...", "releaseDate": "2020-01-01", "msrp": 69, "description": "Reliable DDR4 memory for budget and older builds.", "prices": [{"retailer": "Amazon", "price": 55, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "ram", "capacity": 16, "speed": 3200, "ddrGeneration": "DDR4", "casLatency": 16, "kitSize": 2, "modules": "2x8GB", "voltage": 1.2, "heatspreader": True, "rgb": False},
        ]

    def process_item(self, raw: dict) -> dict | None:
        if not raw.get("name"):
            return None
        if raw.get("type") == "ram" and raw.get("capacity"):
            return raw
        return raw
