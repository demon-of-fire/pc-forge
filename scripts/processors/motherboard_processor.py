import logging
from datetime import datetime, timezone
from pathlib import Path

from .base_processor import BaseProcessor, DATA_DIR
from scrapers.pcpartpicker import scrape_product_list, match_to_existing

logger = logging.getLogger(__name__)


class MotherboardProcessor(BaseProcessor):
    CATEGORY = "motherboards"

    def fetch_data(self) -> list[dict]:
        scraped = scrape_product_list("motherboards", max_pages=3)
        existing = self._load_existing(DATA_DIR / "motherboards.json")
        if scraped and existing:
            updated, new_prods = match_to_existing(scraped, existing)
            logger.info("Matched %d existing, found %d new motherboards", len(updated), len(new_prods))
            return updated
        return scraped

    def seed_data(self) -> list[dict]:
        return [
            {"id": "mb-asus-b650-plus", "slug": "asus-prime-b650-plus", "name": "ASUS Prime B650-Plus", "manufacturer": "ASUS", "image": "/images/motherboards/b650-plus.jpg", "officialUrl": "https://www.asus.com/motherboards-components/motherboards/prime/prime-b650-plus/", "releaseDate": "2022-09-01", "msrp": 199, "description": "A reliable AM5 motherboard for Ryzen 7000 series.", "prices": [{"retailer": "Amazon", "price": 179, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "motherboard", "socket": "AM5", "chipset": "B650", "ddrGeneration": "DDR5", "ramSlots": 4, "maxRam": 128, "pcieSlots": [{"version": "PCIe 4.0", "x": 16}], "m2Slots": 2, "sataPorts": 4, "usbPorts": {"usb2": 4, "usb3": 6, "usbC": 1}, "formFactor": "ATX", "wifiVersion": "Wi-Fi 6", "bluetoothVersion": "5.2"},
            {"id": "mb-msi-z790-tomahawk", "slug": "msi-mag-z790-tomahawk", "name": "MSI MAG Z790 Tomahawk WiFi", "manufacturer": "MSI", "image": "/images/motherboards/z790-tomahawk.jpg", "officialUrl": "https://www.msi.com/Motherboard/MAG-Z790-TOMAHAWK-WIFI", "releaseDate": "2022-10-01", "msrp": 289, "description": "High-performance Z790 board for Intel 14th Gen.", "prices": [{"retailer": "Amazon", "price": 259, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "motherboard", "socket": "LGA1700", "chipset": "Z790", "ddrGeneration": "DDR5", "ramSlots": 4, "maxRam": 192, "pcieSlots": [{"version": "PCIe 5.0", "x": 16}], "m2Slots": 4, "sataPorts": 6, "usbPorts": {"usb2": 4, "usb3": 8, "usbC": 2}, "formFactor": "ATX", "wifiVersion": "Wi-Fi 6E", "bluetoothVersion": "5.3"},
            {"id": "mb-gigabyte-a620i", "slug": "gigabyte-a620i-ax", "name": "Gigabyte A620I AX", "manufacturer": "Gigabyte", "image": "/images/motherboards/a620i.jpg", "officialUrl": "https://www.gigabyte.com/...", "releaseDate": "2023-01-01", "msrp": 159, "description": "Compact ITX motherboard for budget AM5 builds.", "prices": [{"retailer": "Amazon", "price": 149, "currency": "GBP", "url": "https://amazon.co.uk/...", "availability": "in-stock", "lastChecked": "2026-07-10"}], "type": "motherboard", "socket": "AM5", "chipset": "A620", "ddrGeneration": "DDR5", "ramSlots": 2, "maxRam": 64, "pcieSlots": [{"version": "PCIe 4.0", "x": 16}], "m2Slots": 2, "sataPorts": 2, "usbPorts": {"usb2": 2, "usb3": 4, "usbC": 1}, "formFactor": "Mini-ITX", "wifiVersion": "Wi-Fi 6", "bluetoothVersion": "5.2"},
        ]

    def process_item(self, raw: dict) -> dict | None:
        if not raw.get("name"):
            return None
        if raw.get("type") == "motherboard" and raw.get("socket"):
            return raw
        return raw
