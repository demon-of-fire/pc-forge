import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for cooler data:
# - https://pcpartpicker.com/products/cpu-cooler/specs
# - https://www.techpowerup.com/review/
# - https://www.tom's hardware.com/best-picks/best-cpu-coolers

SAMPLE_COOLERS = [
    {
        "id": "cooler-nzxt-kraken-x73",
        "slug": "nzxt-kraken-x73-rgb",
        "name": "NZXT Kraken X73 RGB 360mm AIO",
        "type": "cooler",
        "manufacturer": "NZXT",
        "description": "Premium 360mm AIO liquid cooler with customizable LCD display and RGB.",
        "image": "https://pcpartpicker.com/static/placeholder/kraken-x73.png",
        "releaseDate": "2021-08-01",
        "msrp": 279.99,
        "prices": [],
        "specs": {
            "type": "AIO Liquid",
            "radiatorSize": "360mm",
            "fanSize": "3x 120mm",
            "fanSpeed": "500-2000 RPM",
            "noiseLevel": "21-36 dBA",
            "pumpSpeed": "800-2800 RPM",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x; AMD AM5, AM4",
            "tdpRating": "300W+",
            "rgb": True,
            "display": "LCD",
            "tubeLength": "400mm",
            "warranty": "6 years",
        },
    },
    {
        "id": "cooler-arctic-liquid-freezer-ii-360",
        "slug": "arctic-liquid-freezer-ii-360",
        "name": "Arctic Liquid Freezer II 360",
        "type": "cooler",
        "manufacturer": "Arctic",
        "description": "Top-performing 360mm AIO with thick radiator and exceptional thermal performance.",
        "image": "https://pcpartpicker.com/static/placeholder/liquid-freezer-ii.png",
        "releaseDate": "2020-05-01",
        "msrp": 129.99,
        "prices": [],
        "specs": {
            "type": "AIO Liquid",
            "radiatorSize": "360mm",
            "fanSize": "3x 120mm P12",
            "fanSpeed": "200-1800 RPM",
            "noiseLevel": "22.3 dBA",
            "pumpSpeed": "2000-3000 RPM",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x, 2066; AMD AM5, AM4",
            "tdpRating": "300W+",
            "rgb": False,
            "display": "None",
            "tubeLength": "320mm",
            "warranty": "6 years",
        },
    },
    {
        "id": "cooler-noctua-nh-d15",
        "slug": "noctua-nh-d15",
        "name": "Noctua NH-D15",
        "type": "cooler",
        "manufacturer": "Noctua",
        "description": "Legendary dual-tower air cooler with near-silent operation.",
        "image": "https://pcpartpicker.com/static/placeholder/nh-d15.png",
        "releaseDate": "2014-05-01",
        "msrp": 109.99,
        "prices": [],
        "specs": {
            "type": "Air Tower",
            "heatpipes": 6,
            "fanSize": "2x 140mm NF-A15",
            "fanSpeed": "300-1500 RPM",
            "noiseLevel": "19.2-24.6 dBA",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x, 2066; AMD AM5, AM4",
            "tdpRating": "250W",
            "rgb": False,
            "dimensions": "165 x 150 x 161 mm",
            "weight": "1320g",
            "warranty": "6 years",
        },
    },
    {
        "id": "cooler-corsair-h150i-elite-capellix",
        "slug": "corsair-h150i-elite-capellix",
        "name": "Corsair iCUE H150i ELITE CAPELLIX 360mm AIO",
        "type": "cooler",
        "manufacturer": "Corsair",
        "description": "High-performance 360mm AIO with Capellix RGB LEDs and magnetic levitation fans.",
        "image": "https://pcpartpicker.com/static/placeholder/h150i-capellix.png",
        "releaseDate": "2021-03-01",
        "msrp": 189.99,
        "prices": [],
        "specs": {
            "type": "AIO Liquid",
            "radiatorSize": "360mm",
            "fanSize": "3x 120mm ML RGB",
            "fanSpeed": "400-2400 RPM",
            "noiseLevel": "10-36 dBA",
            "pumpSpeed": "2800 RPM",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x, 2066; AMD AM5, AM4",
            "tdpRating": "300W+",
            "rgb": True,
            "display": "None",
            "tubeLength": "380mm",
            "warranty": "5 years",
        },
    },
    {
        "id": "cooler-be-quiet-dark-rock-pro-4",
        "slug": "be-quiet-dark-rock-pro-4",
        "name": "be quiet! Dark Rock Pro 4",
        "type": "cooler",
        "manufacturer": "be quiet!",
        "description": "Premium dual-tower air cooler with virtually inaudible operation.",
        "image": "https://pcpartpicker.com/static/placeholder/dark-rock-pro-4.png",
        "releaseDate": "2019-03-01",
        "msrp": 89.99,
        "prices": [],
        "specs": {
            "type": "Air Tower",
            "heatpipes": 7,
            "fanSize": "1x 120mm + 1x 135mm Silent Wings",
            "fanSpeed": "Up to 1500 RPM",
            "noiseLevel": "12.8-24.3 dBA",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x, 2066; AMD AM5, AM4",
            "tdpRating": "250W",
            "rgb": False,
            "dimensions": "145.7 x 136 x 162.8 mm",
            "weight": "1130g",
            "warranty": "3 years",
        },
    },
    {
        "id": "cooler-deepcool-ak620",
        "slug": "deepcool-ak620",
        "name": "DeepCool AK620",
        "type": "cooler",
        "manufacturer": "DeepCool",
        "description": "Value-oriented dual-tower air cooler with excellent thermal performance.",
        "image": "https://pcpartpicker.com/static/placeholder/ak620.png",
        "releaseDate": "2022-01-01",
        "msrp": 49.99,
        "prices": [],
        "specs": {
            "type": "Air Tower",
            "heatpipes": 6,
            "fanSize": "2x 120mm FK120",
            "fanSpeed": "500-1850 RPM",
            "noiseLevel": "28 dBA",
            "socketCompatibility": "Intel LGA 1700, 1200, 115x; AMD AM5, AM4",
            "tdpRating": "260W",
            "rgb": False,
            "dimensions": "129 x 138 x 160 mm",
            "weight": "1456g",
            "warranty": "3 years",
        },
    },
]


class CoolerProcessor(BaseProcessor):
    CATEGORY = "coolers"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed cooler data (scraping not yet implemented)")
        return SAMPLE_COOLERS

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("Cooler item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "cooler",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
