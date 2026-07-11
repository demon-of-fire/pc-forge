import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for CPU data:
# - https://pcpartpicker.com/products/cpu/specs
# - https://www.techpowerup.com/review/intel-core-i9-14900k/
# - https://nanoreview.net/en/cpu-list

SAMPLE_CPUS = [
    {
        "id": "cpu-amd-ryzen-9-7950x",
        "slug": "amd-ryzen-9-7950x",
        "name": "AMD Ryzen 9 7950X",
        "type": "cpu",
        "manufacturer": "AMD",
        "description": "16-core, 32-thread desktop processor for enthusiast performance.",
        "image": "https://pcpartpicker.com/static/placeholder/ryzen9-7950x.png",
        "releaseDate": "2022-09-27",
        "msrp": 699.99,
        "prices": [],
        "specs": {
            "cores": 16,
            "threads": 32,
            "baseClock": "4.5 GHz",
            "boostClock": "5.7 GHz",
            "tdp": 170,
            "socket": "AM5",
            "architecture": "Zen 4",
            "l3Cache": "64 MB",
            "integratedGraphics": False,
            "processNode": "5 nm",
        },
        "gamingScore": 93,
        "productivityScore": 98,
        "aiScore": 70,
    },
    {
        "id": "cpu-amd-ryzen-9-7900x",
        "slug": "amd-ryzen-9-7900x",
        "name": "AMD Ryzen 9 7900X",
        "type": "cpu",
        "manufacturer": "AMD",
        "description": "12-core, 24-thread desktop processor with excellent multi-threaded performance.",
        "image": "https://pcpartpicker.com/static/placeholder/ryzen9-7900x.png",
        "releaseDate": "2022-09-27",
        "msrp": 549.99,
        "prices": [],
        "specs": {
            "cores": 12,
            "threads": 24,
            "baseClock": "4.7 GHz",
            "boostClock": "5.6 GHz",
            "tdp": 170,
            "socket": "AM5",
            "architecture": "Zen 4",
            "l3Cache": "64 MB",
            "integratedGraphics": False,
            "processNode": "5 nm",
        },
        "gamingScore": 90,
        "productivityScore": 90,
        "aiScore": 60,
    },
    {
        "id": "cpu-amd-ryzen-7-7800x3d",
        "slug": "amd-ryzen-7-7800x3d",
        "name": "AMD Ryzen 7 7800X3D",
        "type": "cpu",
        "manufacturer": "AMD",
        "description": "8-core gaming processor with 3D V-Cache technology.",
        "image": "https://pcpartpicker.com/static/placeholder/ryzen7-7800x3d.png",
        "releaseDate": "2023-04-06",
        "msrp": 449.99,
        "prices": [],
        "specs": {
            "cores": 8,
            "threads": 16,
            "baseClock": "4.2 GHz",
            "boostClock": "5.0 GHz",
            "tdp": 120,
            "socket": "AM5",
            "architecture": "Zen 4",
            "l3Cache": "96 MB",
            "integratedGraphics": False,
            "processNode": "5 nm",
        },
        "gamingScore": 97,
        "productivityScore": 72,
        "aiScore": 50,
    },
    {
        "id": "cpu-amd-ryzen-5-7600x",
        "slug": "amd-ryzen-5-7600x",
        "name": "AMD Ryzen 5 7600X",
        "type": "cpu",
        "manufacturer": "AMD",
        "description": "6-core, 12-thread mainstream desktop processor.",
        "image": "https://pcpartpicker.com/static/placeholder/ryzen5-7600x.png",
        "releaseDate": "2022-09-27",
        "msrp": 299.99,
        "prices": [],
        "specs": {
            "cores": 6,
            "threads": 12,
            "baseClock": "4.7 GHz",
            "boostClock": "5.3 GHz",
            "tdp": 105,
            "socket": "AM5",
            "architecture": "Zen 4",
            "l3Cache": "32 MB",
            "integratedGraphics": False,
            "processNode": "5 nm",
        },
        "gamingScore": 83,
        "productivityScore": 62,
        "aiScore": 40,
    },
    {
        "id": "cpu-intel-core-i9-14900k",
        "slug": "intel-core-i9-14900k",
        "name": "Intel Core i9-14900K",
        "type": "cpu",
        "manufacturer": "Intel",
        "description": "24-core hybrid architecture desktop processor with high clock speeds.",
        "image": "https://pcpartpicker.com/static/placeholder/i9-14900k.png",
        "releaseDate": "2023-10-17",
        "msrp": 589.99,
        "prices": [],
        "specs": {
            "cores": 24,
            "threads": 32,
            "baseClock": "3.2 GHz",
            "boostClock": "6.0 GHz",
            "tdp": 253,
            "socket": "LGA 1700",
            "architecture": "Raptor Lake",
            "l3Cache": "36 MB",
            "integratedGraphics": True,
            "processNode": "Intel 7",
        },
        "gamingScore": 95,
        "productivityScore": 92,
        "aiScore": 75,
    },
    {
        "id": "cpu-intel-core-i7-14700k",
        "slug": "intel-core-i7-14700k",
        "name": "Intel Core i7-14700K",
        "type": "cpu",
        "manufacturer": "Intel",
        "description": "20-core desktop processor with strong gaming and productivity performance.",
        "image": "https://pcpartpicker.com/static/placeholder/i7-14700k.png",
        "releaseDate": "2023-10-17",
        "msrp": 409.99,
        "prices": [],
        "specs": {
            "cores": 20,
            "threads": 28,
            "baseClock": "3.4 GHz",
            "boostClock": "5.6 GHz",
            "tdp": 253,
            "socket": "LGA 1700",
            "architecture": "Raptor Lake",
            "l3Cache": "33 MB",
            "integratedGraphics": True,
            "processNode": "Intel 7",
        },
        "gamingScore": 91,
        "productivityScore": 85,
        "aiScore": 65,
    },
    {
        "id": "cpu-intel-core-i5-14600k",
        "slug": "intel-core-i5-14600k",
        "name": "Intel Core i5-14600K",
        "type": "cpu",
        "manufacturer": "Intel",
        "description": "14-core mainstream desktop processor offering great value.",
        "image": "https://pcpartpicker.com/static/placeholder/i5-14600k.png",
        "releaseDate": "2023-10-17",
        "msrp": 319.99,
        "prices": [],
        "specs": {
            "cores": 14,
            "threads": 20,
            "baseClock": "3.5 GHz",
            "boostClock": "5.3 GHz",
            "tdp": 181,
            "socket": "LGA 1700",
            "architecture": "Raptor Lake",
            "l3Cache": "24 MB",
            "integratedGraphics": True,
            "processNode": "Intel 7",
        },
        "gamingScore": 85,
        "productivityScore": 75,
        "aiScore": 55,
    },
]


class CPUProcessor(BaseProcessor):
    CATEGORY = "cpus"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed CPU data (scraping not yet implemented)")
        return SAMPLE_CPUS

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("CPU item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "cpu",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }

        if "gamingScore" in raw:
            component["gamingScore"] = float(raw["gamingScore"])
        if "productivityScore" in raw:
            component["productivityScore"] = float(raw["productivityScore"])
        if "aiScore" in raw:
            component["aiScore"] = float(raw["aiScore"])

        return component
