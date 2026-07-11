import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for case data:
# - https://pcpartpicker.com/products/case/specs
# - https://www.techpowerup.com/review/
# - https://www.gamersnexus.net/cases

SAMPLE_CASES = [
    {
        "id": "case-nzxt-h9-flow",
        "slug": "nzxt-h9-flow",
        "name": "NZXT H9 Flow",
        "type": "case",
        "manufacturer": "NZXT",
        "description": "Dual-chamber mid-tower case with excellent airflow and clean cable management.",
        "image": "https://pcpartpicker.com/static/placeholder/h9-flow.png",
        "releaseDate": "2023-01-01",
        "msrp": 164.99,
        "prices": [],
        "specs": {
            "type": "Mid Tower",
            "motherboardSupport": "E-ATX, ATX, Micro-ATX, Mini-ITX",
            "dimensions": "465 x 290 x 459 mm",
            "weight": "10.2 kg",
            "frontIO": "1x USB-C, 2x USB-A, 1x Audio",
            "expansionSlots": 7,
            "maxGPULength": "435 mm",
            "maxCPUCoolerHeight": "165 mm",
            "maxPSULength": "250 mm",
            "includedFans": "3x 120mm RGB",
            "fanSupport": "Up to 10x 120mm or 6x 140mm",
            "radiatorSupport": "Up to 360mm top, 360mm side, 240mm bottom",
            "temperedGlass": "Side panel",
            "color": "White",
        },
    },
    {
        "id": "case-lian-li-o11-dynamic-evo",
        "slug": "lian-li-o11-dynamic-evo",
        "name": "Lian Li O11 Dynamic EVO",
        "type": "case",
        "manufacturer": "Lian Li",
        "description": "Versatile dual-chamber case with reversible design for custom loops.",
        "image": "https://pcpartpicker.com/static/placeholder/o11-evo.png",
        "releaseDate": "2022-04-01",
        "msrp": 169.99,
        "prices": [],
        "specs": {
            "type": "Mid Tower",
            "motherboardSupport": "E-ATX, ATX, Micro-ATX, Mini-ITX",
            "dimensions": "464 x 285 x 459 mm",
            "weight": "9.4 kg",
            "frontIO": "1x USB-C, 2x USB-A, 1x Audio",
            "expansionSlots": 7,
            "maxGPULength": "422 mm",
            "maxCPUCoolerHeight": "167 mm",
            "maxPSULength": "250 mm",
            "includedFans": "0",
            "fanSupport": "Up to 10x 120mm or 6x 140mm",
            "radiatorSupport": "Up to 360mm top, 360mm side, 240mm bottom",
            "temperedGlass": "Front and side",
            "color": "Black",
        },
    },
    {
        "id": "case-fractal-design-north",
        "slug": "fractal-design-north",
        "name": "Fractal Design North",
        "type": "case",
        "manufacturer": "Fractal Design",
        "description": "Elegant mid-tower with wood front panel and mesh side for airflow.",
        "image": "https://pcpartpicker.com/static/placeholder/north.png",
        "releaseDate": "2023-01-01",
        "msrp": 129.99,
        "prices": [],
        "specs": {
            "type": "Mid Tower",
            "motherboardSupport": "ATX, Micro-ATX, Mini-ITX",
            "dimensions": "447 x 215 x 469 mm",
            "weight": "7.6 kg",
            "frontIO": "1x USB-C, 2x USB-A, 1x Audio",
            "expansionSlots": 7,
            "maxGPULength": "355 mm",
            "maxCPUCoolerHeight": "170 mm",
            "maxPSULength": "250 mm",
            "includedFans": "2x 140mm (front), 1x 120mm (rear)",
            "fanSupport": "Up to 6x 120mm or 4x 140mm",
            "radiatorSupport": "Up to 240mm top, 360mm front",
            "temperedGlass": "Side panel",
            "color": "Black / Walnut",
        },
    },
    {
        "id": "case-cooler-master-500-mesh",
        "slug": "cooler-master-td500-mesh",
        "name": "Cooler Master TD500 Mesh",
        "type": "case",
        "manufacturer": "Cooler Master",
        "description": "Mesh front panel case with ARGB fans and great cooling potential.",
        "image": "https://pcpartpicker.com/static/placeholder/td500-mesh.png",
        "releaseDate": "2020-06-01",
        "msrp": 99.99,
        "prices": [],
        "specs": {
            "type": "Mid Tower",
            "motherboardSupport": "ATX, Micro-ATX, Mini-ITX",
            "dimensions": "493 x 217 x 468 mm",
            "weight": "6.3 kg",
            "frontIO": "2x USB-A, 1x Audio",
            "expansionSlots": 7,
            "maxGPULength": "410 mm",
            "maxCPUCoolerHeight": "165 mm",
            "maxPSULength": "180 mm",
            "includedFans": "3x 120mm ARGB",
            "fanSupport": "Up to 6x 120mm",
            "radiatorSupport": "Up to 360mm front, 240mm top",
            "temperedGlass": "Side panel",
            "color": "Black",
        },
    },
    {
        "id": "case-phanteks-enthoo-719",
        "slug": "phanteks-enthoo-719",
        "name": "Phanteks Enthoo 719",
        "type": "case",
        "manufacturer": "Phanteks",
        "description": "Full-tower case supporting dual systems and E-ATX motherboards.",
        "image": "https://pcpartpicker.com/static/placeholder/enthoo-719.png",
        "releaseDate": "2019-05-01",
        "msrp": 189.99,
        "prices": [],
        "specs": {
            "type": "Full Tower",
            "motherboardSupport": "E-ATX, SSI-EEB, ATX, Micro-ATX, Mini-ITX",
            "dimensions": "595 x 240 x 580 mm",
            "weight": "15.2 kg",
            "frontIO": "1x USB-C, 4x USB-A, 1x Audio",
            "expansionSlots": 12,
            "maxGPULength": "503 mm",
            "maxCPUCoolerHeight": "195 mm",
            "maxPSULength": "350 mm",
            "includedFans": "3x 140mm PH-F140SP",
            "fanSupport": "Up to 12x 120mm or 11x 140mm",
            "radiatorSupport": "Up to 480mm side, 360mm front, 120mm rear",
            "temperedGlass": "Side panel",
            "color": "Black",
        },
    },
]


class CaseProcessor(BaseProcessor):
    CATEGORY = "cases"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed case data (scraping not yet implemented)")
        return SAMPLE_CASES

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("Case item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "case",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
