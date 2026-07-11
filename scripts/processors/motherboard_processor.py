import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for motherboard data:
# - https://pcpartpicker.com/products/motherboard/specs
# - https://www.techpowerup.com/review/
# - https://www.motherboardorbit.com/

SAMPLE_MOTHERBOARDS = [
    {
        "id": "mb-asus-rog-crosshair-x670e-hero",
        "slug": "asus-rog-crosshair-x670e-hero",
        "name": "ASUS ROG Crosshair X670E Hero",
        "type": "motherboard",
        "manufacturer": "ASUS",
        "description": "High-end AM5 motherboard with PCIe 5.0 support and premium VRM.",
        "image": "https://pcpartpicker.com/static/placeholder/crosshair-x670e.png",
        "releaseDate": "2022-09-27",
        "msrp": 699.99,
        "prices": [],
        "specs": {
            "socket": "AM5",
            "chipset": "X670E",
            "formFactor": "ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "2x PCIe 5.0 x16, 1x PCIe 4.0 x4",
            "m2Slots": 3,
            "sataPorts": 8,
            "usbPorts": "2x USB4, 12x USB 3.2",
            "wifi": "Wi-Fi 6E",
            "ethernet": "2.5 GbE + 1 GbE",
            "audio": "Realtek ALC4082",
        },
    },
    {
        "id": "mb-msi-meg-x670e-ace",
        "slug": "msi-meg-x670e-ace",
        "name": "MSI MEG X670E ACE",
        "type": "motherboard",
        "manufacturer": "MSI",
        "description": "Premium X670E motherboard with exceptional VRM and connectivity.",
        "image": "https://pcpartpicker.com/static/placeholder/meg-x670e-ace.png",
        "releaseDate": "2022-09-27",
        "msrp": 699.99,
        "prices": [],
        "specs": {
            "socket": "AM5",
            "chipset": "X670E",
            "formFactor": "E-ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "2x PCIe 5.0 x16, 1x PCIe 4.0 x4",
            "m2Slots": 4,
            "sataPorts": 6,
            "usbPorts": "2x USB4, 10x USB 3.2",
            "wifi": "Wi-Fi 6E",
            "ethernet": "2.5 GbE",
            "audio": "Realtek ALC4082",
        },
    },
    {
        "id": "mb-gigabyte-x670e-aorus-master",
        "slug": "gigabyte-x670e-aorus-master",
        "name": "Gigabyte X670E AORUS Master",
        "type": "motherboard",
        "manufacturer": "Gigabyte",
        "description": "Feature-rich X670E board with strong VRM and multiple M.2 slots.",
        "image": "https://pcpartpicker.com/static/placeholder/x670e-aorus-master.png",
        "releaseDate": "2022-09-27",
        "msrp": 499.99,
        "prices": [],
        "specs": {
            "socket": "AM5",
            "chipset": "X670E",
            "formFactor": "ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "1x PCIe 5.0 x16, 2x PCIe 4.0 x16",
            "m2Slots": 4,
            "sataPorts": 4,
            "usbPorts": "1x USB4, 12x USB 3.2",
            "wifi": "Wi-Fi 6E",
            "ethernet": "2.5 GbE",
            "audio": "Realtek ALC1220-VB",
        },
    },
    {
        "id": "mb-asus-rog-strix-b650e-f",
        "slug": "asus-rog-strix-b650e-f-gaming-wifi",
        "name": "ASUS ROG STRIX B650E-F Gaming WiFi",
        "type": "motherboard",
        "manufacturer": "ASUS",
        "description": "Mid-range B650E board with solid features for gaming builds.",
        "image": "https://pcpartpicker.com/static/placeholder/strix-b650e-f.png",
        "releaseDate": "2022-09-27",
        "msrp": 279.99,
        "prices": [],
        "specs": {
            "socket": "AM5",
            "chipset": "B650E",
            "formFactor": "ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "1x PCIe 5.0 x16, 1x PCIe 4.0 x16",
            "m2Slots": 3,
            "sataPorts": 4,
            "usbPorts": "1x USB 3.2 Gen 2x2, 8x USB 3.2",
            "wifi": "Wi-Fi 6E",
            "ethernet": "2.5 GbE",
            "audio": "Realtek ALC4080",
        },
    },
    {
        "id": "mb-msi-pro-z790-p",
        "slug": "msi-pro-z790-p-wifi",
        "name": "MSI PRO Z790-P WiFi",
        "type": "motherboard",
        "manufacturer": "MSI",
        "description": "Affordable Z790 board with solid connectivity for Intel builds.",
        "image": "https://pcpartpicker.com/static/placeholder/pro-z790-p.png",
        "releaseDate": "2022-09-27",
        "msrp": 229.99,
        "prices": [],
        "specs": {
            "socket": "LGA 1700",
            "chipset": "Z790",
            "formFactor": "ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "1x PCIe 5.0 x16, 2x PCIe 4.0 x16",
            "m2Slots": 4,
            "sataPorts": 6,
            "usbPorts": "1x USB 3.2 Gen 2x2, 6x USB 3.2",
            "wifi": "Wi-Fi 6E",
            "ethernet": "2.5 GbE",
            "audio": "Realtek ALC897",
        },
    },
    {
        "id": "mb-asus-tuf-gaming-b760m",
        "slug": "asus-tuf-gaming-b760m-plus-wifi",
        "name": "ASUS TUF Gaming B760M-PLUS WiFi",
        "type": "motherboard",
        "manufacturer": "ASUS",
        "description": "Budget-friendly mATX B760 board with TUF durability.",
        "image": "https://pcpartpicker.com/static/placeholder/tuf-b760m.png",
        "releaseDate": "2023-01-03",
        "msrp": 179.99,
        "prices": [],
        "specs": {
            "socket": "LGA 1700",
            "chipset": "B760",
            "formFactor": "Micro-ATX",
            "memorySlots": 4,
            "maxMemory": 128,
            "memoryType": "DDR5",
            "pcieSlots": "1x PCIe 4.0 x16, 1x PCIe 3.0 x1",
            "m2Slots": 2,
            "sataPorts": 4,
            "usbPorts": "1x USB 3.2 Gen 2x2, 6x USB 3.2",
            "wifi": "Wi-Fi 6",
            "ethernet": "1 GbE",
            "audio": "Realtek ALC897",
        },
    },
]


class MotherboardProcessor(BaseProcessor):
    CATEGORY = "motherboards"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed motherboard data (scraping not yet implemented)")
        return SAMPLE_MOTHERBOARDS

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("Motherboard item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "motherboard",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
