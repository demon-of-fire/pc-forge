import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for RAM data:
# - https://pcpartpicker.com/products/memory/specs
# - https://www.techpowerup.com/review/
# - https://www.gskill.com/

SAMPLE_RAM = [
    {
        "id": "ram-gskill-trident-z5-6000-32gb",
        "slug": "gskill-trident-z5-ddr5-6000-cl30-32gb",
        "name": "G.Skill Trident Z5 DDR5-6000 CL30 32 GB (2x16 GB)",
        "type": "ram",
        "manufacturer": "G.Skill",
        "description": "High-performance DDR5 kit with tight timings for enthusiast builds.",
        "image": "https://pcpartpicker.com/static/placeholder/trident-z5.png",
        "releaseDate": "2022-06-01",
        "msrp": 139.99,
        "prices": [],
        "specs": {
            "capacity": "32 GB (2x16 GB)",
            "type": "DDR5",
            "speed": "6000 MHz",
            "casLatency": "CL30",
            "voltage": "1.35V",
            "heatSpreader": "Aluminum",
            "rgb": True,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
    {
        "id": "ram-corsair-dominator-platinum-6400-32gb",
        "slug": "corsair-dominator-platinum-ddr5-6400-cl32-32gb",
        "name": "Corsair Dominator Platinum DDR5-6400 CL32 32 GB (2x16 GB)",
        "type": "ram",
        "manufacturer": "Corsair",
        "description": "Premium DDR5 memory with DHX cooling and Capellix RGB LEDs.",
        "image": "https://pcpartpicker.com/static/placeholder/dominator-plat.png",
        "releaseDate": "2022-06-01",
        "msrp": 189.99,
        "prices": [],
        "specs": {
            "capacity": "32 GB (2x16 GB)",
            "type": "DDR5",
            "speed": "6400 MHz",
            "casLatency": "CL32",
            "voltage": "1.40V",
            "heatSpreader": "Aluminum DHX",
            "rgb": True,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
    {
        "id": "ram-gskill-flare-x5-6000-32gb",
        "slug": "gskill-flare-x5-ddr5-6000-cl30-32gb",
        "name": "G.Skill Flare X5 DDR5-6000 CL30 32 GB (2x16 GB)",
        "type": "ram",
        "manufacturer": "G.Skill",
        "description": "AMD-optimized DDR5 kit with EXPO profiles for AM5 platforms.",
        "image": "https://pcpartpicker.com/static/placeholder/flare-x5.png",
        "releaseDate": "2022-08-01",
        "msrp": 119.99,
        "prices": [],
        "specs": {
            "capacity": "32 GB (2x16 GB)",
            "type": "DDR5",
            "speed": "6000 MHz",
            "casLatency": "CL30",
            "voltage": "1.35V",
            "heatSpreader": "Aluminum",
            "rgb": False,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
    {
        "id": "ram-corsair-vengeance-5600-64gb",
        "slug": "corsair-vengeance-ddr5-5600-cl36-64gb",
        "name": "Corsair Vengeance DDR5-5600 CL36 64 GB (2x32 GB)",
        "type": "ram",
        "manufacturer": "Corsair",
        "description": "High-capacity DDR5 kit for workstations and content creation.",
        "image": "https://pcpartpicker.com/static/placeholder/vengeance-ddr5.png",
        "releaseDate": "2022-06-01",
        "msrp": 219.99,
        "prices": [],
        "specs": {
            "capacity": "64 GB (2x32 GB)",
            "type": "DDR5",
            "speed": "5600 MHz",
            "casLatency": "CL36",
            "voltage": "1.25V",
            "heatSpreader": "Aluminum",
            "rgb": False,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
    {
        "id": "ram-gskill-ripjaws-s5-5200-32gb",
        "slug": "gskill-ripjaws-s5-ddr5-5200-cl36-32gb",
        "name": "G.Skill Ripjaws S5 DDR5-5200 CL36 32 GB (2x16 GB)",
        "type": "ram",
        "manufacturer": "G.Skill",
        "description": "Budget-friendly DDR5 kit with solid performance for mainstream builds.",
        "image": "https://pcpartpicker.com/static/placeholder/ripjaws-s5.png",
        "releaseDate": "2022-06-01",
        "msrp": 79.99,
        "prices": [],
        "specs": {
            "capacity": "32 GB (2x16 GB)",
            "type": "DDR5",
            "speed": "5200 MHz",
            "casLatency": "CL36",
            "voltage": "1.25V",
            "heatSpreader": "Aluminum",
            "rgb": False,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
    {
        "id": "ram-teamgroup-t-force-delta-6400-32gb",
        "slug": "teamgroup-t-force-delta-rgb-ddr5-6400-cl32-32gb",
        "name": "TeamGroup T-Force Delta RGB DDR5-6400 CL32 32 GB (2x16 GB)",
        "type": "ram",
        "manufacturer": "TeamGroup",
        "description": "RGB DDR5 kit with high speed and aggressive timings.",
        "image": "https://pcpartpicker.com/static/placeholder/t-force-delta.png",
        "releaseDate": "2023-01-01",
        "msrp": 149.99,
        "prices": [],
        "specs": {
            "capacity": "32 GB (2x16 GB)",
            "type": "DDR5",
            "speed": "6400 MHz",
            "casLatency": "CL32",
            "voltage": "1.40V",
            "heatSpreader": "Aluminum",
            "rgb": True,
            "xmp": "XMP 3.0",
            "amdExpo": True,
        },
    },
]


class RAMProcessor(BaseProcessor):
    CATEGORY = "ram"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed RAM data (scraping not yet implemented)")
        return SAMPLE_RAM

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("RAM item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "ram",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
