import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for GPU data:
# - https://pcpartpicker.com/products/video-card/specs
# - https://www.techpowerup.com/gpu-specs/
# - https://videocardz.net/

SAMPLE_GPUS = [
    {
        "id": "gpu-nvidia-rtx-4090",
        "slug": "nvidia-geforce-rtx-4090",
        "name": "NVIDIA GeForce RTX 4090",
        "type": "gpu",
        "manufacturer": "NVIDIA",
        "description": "Flagship Ada Lovelace GPU with 24 GB GDDR6X memory.",
        "image": "https://pcpartpicker.com/static/placeholder/rtx4090.png",
        "releaseDate": "2022-10-12",
        "msrp": 1599.99,
        "prices": [],
        "specs": {
            "cudaCores": 16384,
            "memory": "24 GB GDDR6X",
            "memoryBus": "384-bit",
            "baseClock": "2235 MHz",
            "boostClock": "2520 MHz",
            "tdp": 450,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "dlss": "DLSS 3",
        },
        "gamingScore": 100,
        "productivityScore": 100,
        "aiScore": 100,
    },
    {
        "id": "gpu-nvidia-rtx-4080-super",
        "slug": "nvidia-geforce-rtx-4080-super",
        "name": "NVIDIA GeForce RTX 4080 Super",
        "type": "gpu",
        "manufacturer": "NVIDIA",
        "description": "High-end Ada Lovelace GPU with 16 GB GDDR6X memory.",
        "image": "https://pcpartpicker.com/static/placeholder/rtx4080super.png",
        "releaseDate": "2024-01-31",
        "msrp": 999.99,
        "prices": [],
        "specs": {
            "cudaCores": 10240,
            "memory": "16 GB GDDR6X",
            "memoryBus": "256-bit",
            "baseClock": "2295 MHz",
            "boostClock": "2550 MHz",
            "tdp": 320,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "dlss": "DLSS 3",
        },
        "gamingScore": 88,
        "productivityScore": 82,
        "aiScore": 80,
    },
    {
        "id": "gpu-nvidia-rtx-4070-ti-super",
        "slug": "nvidia-geforce-rtx-4070-ti-super",
        "name": "NVIDIA GeForce RTX 4070 Ti Super",
        "type": "gpu",
        "manufacturer": "NVIDIA",
        "description": "Upper mid-range GPU with 16 GB GDDR6X memory.",
        "image": "https://pcpartpicker.com/static/placeholder/rtx4070tisuper.png",
        "releaseDate": "2024-01-24",
        "msrp": 799.99,
        "prices": [],
        "specs": {
            "cudaCores": 8448,
            "memory": "16 GB GDDR6X",
            "memoryBus": "256-bit",
            "baseClock": "2340 MHz",
            "boostClock": "2610 MHz",
            "tdp": 285,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "dlss": "DLSS 3",
        },
        "gamingScore": 80,
        "productivityScore": 72,
        "aiScore": 70,
    },
    {
        "id": "gpu-nvidia-rtx-4070-super",
        "slug": "nvidia-geforce-rtx-4070-super",
        "name": "NVIDIA GeForce RTX 4070 Super",
        "type": "gpu",
        "manufacturer": "NVIDIA",
        "description": "Mid-range GPU with 12 GB GDDR6X memory, great value.",
        "image": "https://pcpartpicker.com/static/placeholder/rtx4070super.png",
        "releaseDate": "2024-01-17",
        "msrp": 599.99,
        "prices": [],
        "specs": {
            "cudaCores": 7168,
            "memory": "12 GB GDDR6X",
            "memoryBus": "192-bit",
            "baseClock": "1920 MHz",
            "boostClock": "2475 MHz",
            "tdp": 220,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "dlss": "DLSS 3",
        },
        "gamingScore": 72,
        "productivityScore": 62,
        "aiScore": 58,
    },
    {
        "id": "gpu-amd-rx-7900-xtx",
        "slug": "amd-radeon-rx-7900-xtx",
        "name": "AMD Radeon RX 7900 XTX",
        "type": "gpu",
        "manufacturer": "AMD",
        "description": "Flagship RDNA 3 GPU with 24 GB GDDR6 memory.",
        "image": "https://pcpartpicker.com/static/placeholder/rx7900xtx.png",
        "releaseDate": "2022-12-13",
        "msrp": 999.99,
        "prices": [],
        "specs": {
            "streamProcessors": 6144,
            "memory": "24 GB GDDR6",
            "memoryBus": "384-bit",
            "baseClock": "1855 MHz",
            "boostClock": "2499 MHz",
            "tdp": 355,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "fsr": "FSR 3",
        },
        "gamingScore": 85,
        "productivityScore": 78,
        "aiScore": 60,
    },
    {
        "id": "gpu-amd-rx-7800-xt",
        "slug": "amd-radeon-rx-7800-xt",
        "name": "AMD Radeon RX 7800 XT",
        "type": "gpu",
        "manufacturer": "AMD",
        "description": "Mid-range RDNA 3 GPU with 16 GB GDDR6 memory.",
        "image": "https://pcpartpicker.com/static/placeholder/rx7800xt.png",
        "releaseDate": "2023-09-06",
        "msrp": 499.99,
        "prices": [],
        "specs": {
            "streamProcessors": 3840,
            "memory": "16 GB GDDR6",
            "memoryBus": "256-bit",
            "baseClock": "1295 MHz",
            "boostClock": "2430 MHz",
            "tdp": 263,
            "interface": "PCIe 4.0 x16",
            "rayTracing": True,
            "fsr": "FSR 3",
        },
        "gamingScore": 72,
        "productivityScore": 58,
        "aiScore": 45,
    },
]


class GPUProcessor(BaseProcessor):
    CATEGORY = "gpus"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed GPU data (scraping not yet implemented)")
        return SAMPLE_GPUS

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("GPU item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "gpu",
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
