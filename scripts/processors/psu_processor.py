import logging
from datetime import datetime, timezone
from pathlib import Path

from .base_processor import BaseProcessor, DATA_DIR
from scrapers.pcpartpicker import scrape_product_list, match_to_existing

logger = logging.getLogger(__name__)


class PSUProcessor(BaseProcessor):
    CATEGORY = "psus"

    def fetch_data(self) -> list[dict]:
        scraped = scrape_product_list("psus", max_pages=3)
        existing = self._load_existing(DATA_DIR / "psus.json")
        if scraped and existing:
            updated, new_prods = match_to_existing(scraped, existing)
            logger.info("Matched %d existing, found %d new PSUs", len(updated), len(new_prods))
            return updated
        return scraped

    def seed_data(self) -> list[dict]:
        return [
            {"id": "psu-corsair-rm850e", "slug": "corsair-rm850e", "name": "Corsair RM850e 850W Gold", "manufacturer": "Corsair", "image": "/images/psus/rm850e.jpg", "officialUrl": "https://www.corsair.com/...", "releaseDate": "2023-01-01", "msrp": 139, "description": "Highly efficient ATX 3.0 power supply for modern GPUs.", "prices": [{"retailer": "Amazon", "price": 119, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "psu", "wattage": 850, "efficiencyRating": "80+ Gold", "modularType": "Full", "fanSize": 120, "length": 140, "cpuConnectors": 2, "gpuConnectors": 4, "sataConnectors": 8, "molexConnectors": 2, "atxVersion": "3.0"},
            {"id": "psu-seasonic-focus-750", "slug": "seasonic-focus-gx-750", "name": "Seasonic Focus GX-750 Gold", "manufacturer": "Seasonic", "image": "/images/psus/focus-750.jpg", "officialUrl": "https://seasonic.com/...", "releaseDate": "2021-01-01", "msrp": 129, "description": "Legendary reliability and performance in a compact size.", "prices": [{"retailer": "Amazon", "price": 109, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "psu", "wattage": 750, "efficiencyRating": "80+ Gold", "modularType": "Full", "fanSize": 120, "length": 140, "cpuConnectors": 2, "gpuConnectors": 3, "sataConnectors": 6, "molexConnectors": 2, "atxVersion": "2.4"},
            {"id": "psu-evga-600w-bronze", "slug": "evga-600w-bronze", "name": "EVGA 600W 80+ Bronze", "manufacturer": "EVGA", "image": "/images/psus/600w-bronze.jpg", "officialUrl": "https://www.evga.com/...", "releaseDate": "2019-01-01", "msrp": 69, "description": "Budget-friendly power supply for basic gaming PCs.", "prices": [{"retailer": "Amazon", "price": 59, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "psu", "wattage": 600, "efficiencyRating": "80+ Bronze", "modularType": "Non-Modular", "fanSize": 120, "length": 140, "cpuConnectors": 1, "gpuConnectors": 2, "sataConnectors": 4, "molexConnectors": 2, "atxVersion": "2.3"},
        ]

    def process_item(self, raw: dict) -> dict | None:
        if not raw.get("name"):
            return None
        if raw.get("type") == "psu" and raw.get("wattage"):
            return raw
        return raw
