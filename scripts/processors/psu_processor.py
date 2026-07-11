import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for PSU data:
# - https://pcpartpicker.com/products/power-supply/specs
# - https://www.techpowerup.com/review/
# - https://www.tom's hardware.com/best-picks/best-psus

SAMPLE_PSUS = [
    {
        "id": "psu-corsair-rm1000x-2023",
        "slug": "corsair-rm1000x-2023",
        "name": "Corsair RM1000x (2023) 1000W 80+ Gold",
        "type": "psu",
        "manufacturer": "Corsair",
        "description": "Fully modular 80 Plus Gold PSU with quiet operation and ATX 3.0 support.",
        "image": "https://pcpartpicker.com/static/placeholder/rm1000x.png",
        "releaseDate": "2023-03-01",
        "msrp": 189.99,
        "prices": [],
        "specs": {
            "wattage": 1000,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "formFactor": "ATX",
            "atx30": True,
            "pcie5Connector": True,
            "fanSize": "135mm",
            "fanBearing": "FDB",
            "protections": "OVP, UVP, OCP, OPP, SCP, OTP",
            "warranty": "10 years",
        },
    },
    {
        "id": "psu-corsair-rm850x-2023",
        "slug": "corsair-rm850x-2023",
        "name": "Corsair RM850x (2023) 850W 80+ Gold",
        "type": "psu",
        "manufacturer": "Corsair",
        "description": "Fully modular 80 Plus Gold PSU ideal for high-end gaming builds.",
        "image": "https://pcpartpicker.com/static/placeholder/rm850x.png",
        "releaseDate": "2023-03-01",
        "msrp": 149.99,
        "prices": [],
        "specs": {
            "wattage": 850,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "formFactor": "ATX",
            "atx30": True,
            "pcie5Connector": True,
            "fanSize": "135mm",
            "fanBearing": "FDB",
            "protections": "OVP, UVP, OCP, OPP, SCP, OTP",
            "warranty": "10 years",
        },
    },
    {
        "id": "psu-seasonic-vertex-gx-1200",
        "slug": "seasonic-vertex-gx-1200",
        "name": "Seasonic VERTEX GX-1200 1200W 80+ Gold",
        "type": "psu",
        "manufacturer": "Seasonic",
        "description": "Premium ATX 3.0 PSU with native 12VHPWR connector and top-tier components.",
        "image": "https://pcpartpicker.com/static/placeholder/vertex-gx-1200.png",
        "releaseDate": "2023-01-01",
        "msrp": 249.99,
        "prices": [],
        "specs": {
            "wattage": 1200,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "formFactor": "ATX",
            "atx30": True,
            "pcie5Connector": True,
            "fanSize": "135mm",
            "fanBearing": "FDB",
            "protections": "OVP, UVP, OCP, OPP, SCP, OTP",
            "warranty": "10 years",
        },
    },
    {
        "id": "psu-evga-supernova-g6-750",
        "slug": "evga-supernova-750-g6",
        "name": "EVGA SuperNOVA 750 G6 750W 80+ Gold",
        "type": "psu",
        "manufacturer": "EVGA",
        "description": "Compact fully modular PSU with excellent value and performance.",
        "image": "https://pcpartpicker.com/static/placeholder/supernova-g6.png",
        "releaseDate": "2021-06-01",
        "msrp": 89.99,
        "prices": [],
        "specs": {
            "wattage": 750,
            "efficiency": "80+ Gold",
            "modular": "Full",
            "formFactor": "ATX",
            "atx30": False,
            "pcie5Connector": False,
            "fanSize": "135mm",
            "fanBearing": "FDB",
            "protections": "OVP, UVP, OCP, OPP, SCP, OTP",
            "warranty": "10 years",
        },
    },
    {
        "id": "psu-be-quiet-dark-power-13-1000",
        "slug": "be-quiet-dark-power-13-1000w",
        "name": "be quiet! Dark Power 13 1000W 80+ Titanium",
        "type": "psu",
        "manufacturer": "be quiet!",
        "description": "Ultra-high-efficiency titanium PSU for silent enthusiast builds.",
        "image": "https://pcpartpicker.com/static/placeholder/dark-power-13.png",
        "releaseDate": "2022-06-01",
        "msrp": 299.99,
        "prices": [],
        "specs": {
            "wattage": 1000,
            "efficiency": "80+ Titanium",
            "modular": "Full",
            "formFactor": "ATX",
            "atx30": True,
            "pcie5Connector": True,
            "fanSize": "135mm",
            "fanBearing": "FDB",
            "protections": "OVP, UVP, OCP, OPP, SCP, OTP",
            "warranty": "10 years",
        },
    },
]


class PSUProcessor(BaseProcessor):
    CATEGORY = "psus"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed PSU data (scraping not yet implemented)")
        return SAMPLE_PSUS

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("PSU item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "psu",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
