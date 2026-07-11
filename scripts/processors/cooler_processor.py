import logging
from datetime import datetime, timezone
from pathlib import Path

from .base_processor import BaseProcessor, DATA_DIR
from scrapers.pcpartpicker import scrape_product_list, match_to_existing

logger = logging.getLogger(__name__)


class CoolerProcessor(BaseProcessor):
    CATEGORY = "coolers"

    def fetch_data(self) -> list[dict]:
        scraped = scrape_product_list("coolers", max_pages=3)
        existing = self._load_existing(DATA_DIR / "coolers.json")
        if scraped and existing:
            updated, new_prods = match_to_existing(scraped, existing)
            logger.info("Matched %d existing, found %d new coolers", len(updated), len(new_prods))
            return updated
        return scraped

    def seed_data(self) -> list[dict]:
        return [
            {"id": "cooler-noctua-nhd15", "slug": "noctua-nh-d15", "name": "Noctua NH-D15", "manufacturer": "Noctua", "image": "/images/cooling/nhd15.jpg", "officialUrl": "https://noctua.at/...", "releaseDate": "2014-01-01", "msrp": 109, "description": "The legendary air cooler known for extreme performance and silence.", "prices": [{"retailer": "Amazon", "price": 99, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "cooler", "coolerType": "Air", "socketCompatibility": ["AM4", "AM5", "LGA1700", "LGA1200"], "height": 165, "fanSize": 140, "fanCount": 2, "radiatorSize": None, "coolingCapacity": 250, "noiseLevel": 30, "tdpRating": 250},
            {"id": "cooler-corsair-h150i", "slug": "corsair-h150i-elite", "name": "Corsair iCUE H150i Elite Capellix XT", "manufacturer": "Corsair", "image": "/images/cooling/h150i.jpg", "officialUrl": "https://corsair.com/...", "releaseDate": "2022-01-01", "msrp": 229, "description": "Premium 360mm AIO cooler for high-TDP processors.", "prices": [{"retailer": "Scan", "price": 219, "currency": "GBP", "url": "https://scan.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "cooler", "coolerType": "AIO Liquid", "socketCompatibility": ["AM4", "AM5", "LGA1700", "LGA1200"], "height": None, "fanSize": 120, "fanCount": 3, "radiatorSize": 360, "coolingCapacity": 300, "noiseLevel": 35, "tdpRating": 300},
            {"id": "cooler-bequiet-darkrock", "slug": "bequiet-dark-rock-pro-4", "name": "be quiet! Dark Rock Pro 4", "manufacturer": "be quiet!", "image": "/images/cooling/darkrockpro4.jpg", "officialUrl": "https://bequiet.com/...", "releaseDate": "2019-01-01", "msrp": 89, "description": "Near-silent air cooling for professional workstations.", "prices": [{"retailer": "Amazon", "price": 79, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "cooler", "coolerType": "Air", "socketCompatibility": ["AM4", "AM5", "LGA1700", "LGA1200"], "height": 160, "fanSize": 120, "fanCount": 2, "radiatorSize": None, "coolingCapacity": 220, "noiseLevel": 25, "tdpRating": 220},
        ]

    def process_item(self, raw: dict) -> dict | None:
        if not raw.get("name"):
            return None
        if raw.get("type") == "cooler" and raw.get("coolerType"):
            return raw
        return raw
