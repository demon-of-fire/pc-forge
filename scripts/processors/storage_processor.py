import logging
from datetime import datetime, timezone

from .base_processor import BaseProcessor

logger = logging.getLogger(__name__)

# Sources for storage data:
# - https://pcpartpicker.com/products/internal-hard-drive/specs
# - https://www.techpowerup.com/review/
# - https://www.tom's hardware.com/best-picks/best-ssds

SAMPLE_STORAGE = [
    {
        "id": "storage-samsung-990-pro-2tb",
        "slug": "samsung-990-pro-2tb",
        "name": "Samsung 990 Pro 2 TB NVMe SSD",
        "type": "storage",
        "manufacturer": "Samsung",
        "description": "Top-tier PCIe 4.0 NVMe SSD with exceptional sequential and random performance.",
        "image": "https://pcpartpicker.com/static/placeholder/990-pro.png",
        "releaseDate": "2022-09-01",
        "msrp": 199.99,
        "prices": [],
        "specs": {
            "capacity": "2 TB",
            "type": "NVMe SSD",
            "interface": "PCIe 4.0 x4",
            "formFactor": "M.2 2280",
            "sequentialRead": "7450 MB/s",
            "sequentialWrite": "6900 MB/s",
            "randomRead": "1400K IOPS",
            "randomWrite": "1550K IOPS",
            "endurance": "1200 TBW",
            "nandType": "TLC V-NAND",
            "cache": "2 GB LPDDR4",
            "warranty": "5 years",
        },
    },
    {
        "id": "storage-samsung-990-pro-1tb",
        "slug": "samsung-990-pro-1tb",
        "name": "Samsung 990 Pro 1 TB NVMe SSD",
        "type": "storage",
        "manufacturer": "Samsung",
        "description": "High-performance PCIe 4.0 NVMe SSD for gaming and creative workloads.",
        "image": "https://pcpartpicker.com/static/placeholder/990-pro-1tb.png",
        "releaseDate": "2022-09-01",
        "msrp": 109.99,
        "prices": [],
        "specs": {
            "capacity": "1 TB",
            "type": "NVMe SSD",
            "interface": "PCIe 4.0 x4",
            "formFactor": "M.2 2280",
            "sequentialRead": "7450 MB/s",
            "sequentialWrite": "6900 MB/s",
            "randomRead": "1200K IOPS",
            "randomWrite": "1550K IOPS",
            "endurance": "600 TBW",
            "nandType": "TLC V-NAND",
            "cache": "1 GB LPDDR4",
            "warranty": "5 years",
        },
    },
    {
        "id": "storage-wd-black-sn850x-2tb",
        "slug": "wd-black-sn850x-2tb",
        "name": "WD Black SN850X 2 TB NVMe SSD",
        "type": "storage",
        "manufacturer": "Western Digital",
        "description": "Fast PCIe 4.0 NVMe drive optimized for gaming with Game Mode 2.0.",
        "image": "https://pcpartpicker.com/static/placeholder/sn850x.png",
        "releaseDate": "2022-08-01",
        "msrp": 179.99,
        "prices": [],
        "specs": {
            "capacity": "2 TB",
            "type": "NVMe SSD",
            "interface": "PCIe 4.0 x4",
            "formFactor": "M.2 2280",
            "sequentialRead": "7300 MB/s",
            "sequentialWrite": "6600 MB/s",
            "randomRead": "1200K IOPS",
            "randomWrite": "1100K IOPS",
            "endurance": "1200 TBW",
            "nandType": "BiCS5 TLC",
            "cache": "2 GB DDR4",
            "warranty": "5 years",
        },
    },
    {
        "id": "storage-crucial-t700-2tb",
        "slug": "crucial-t700-2tb",
        "name": "Crucial T700 2 TB NVMe SSD",
        "type": "storage",
        "manufacturer": "Crucial",
        "description": "PCIe 5.0 NVMe SSD with blistering sequential speeds.",
        "image": "https://pcpartpicker.com/static/placeholder/t700.png",
        "releaseDate": "2023-06-01",
        "msrp": 249.99,
        "prices": [],
        "specs": {
            "capacity": "2 TB",
            "type": "NVMe SSD",
            "interface": "PCIe 5.0 x4",
            "formFactor": "M.2 2280",
            "sequentialRead": "12400 MB/s",
            "sequentialWrite": "11800 MB/s",
            "randomRead": "2200K IOPS",
            "randomWrite": "1500K IOPS",
            "endurance": "1200 TBW",
            "nandType": "232-layer TLC",
            "cache": "DRAM-less HMB",
            "warranty": "5 years",
        },
    },
    {
        "id": "storage-seagate-barracuda-4tb",
        "slug": "seagate-barracuda-4tb",
        "name": "Seagate Barracuda 4 TB HDD",
        "type": "storage",
        "manufacturer": "Seagate",
        "description": "High-capacity mechanical hard drive for mass storage.",
        "image": "https://pcpartpicker.com/static/placeholder/barracuda-4tb.png",
        "releaseDate": "2020-01-01",
        "msrp": 89.99,
        "prices": [],
        "specs": {
            "capacity": "4 TB",
            "type": "HDD",
            "interface": "SATA III",
            "formFactor": "3.5-inch",
            "rpm": 5480,
            "sequentialRead": "190 MB/s",
            "cache": "256 MB",
            "warranty": "2 years",
        },
    },
    {
        "id": "storage-wd-black-sn850x-4tb",
        "slug": "wd-black-sn850x-4tb",
        "name": "WD Black SN850X 4 TB NVMe SSD",
        "type": "storage",
        "manufacturer": "Western Digital",
        "description": "High-capacity PCIe 4.0 NVMe SSD for expansive game libraries.",
        "image": "https://pcpartpicker.com/static/placeholder/sn850x-4tb.png",
        "releaseDate": "2023-10-01",
        "msrp": 299.99,
        "prices": [],
        "specs": {
            "capacity": "4 TB",
            "type": "NVMe SSD",
            "interface": "PCIe 4.0 x4",
            "formFactor": "M.2 2280",
            "sequentialRead": "7300 MB/s",
            "sequentialWrite": "6600 MB/s",
            "randomRead": "1200K IOPS",
            "randomWrite": "1100K IOPS",
            "endurance": "2400 TBW",
            "nandType": "BiCS5 TLC",
            "cache": "DDR4 DRAM",
            "warranty": "5 years",
        },
    },
]


class StorageProcessor(BaseProcessor):
    CATEGORY = "storage"

    def fetch_data(self) -> list[dict]:
        logger.info("Using seed storage data (scraping not yet implemented)")
        return SAMPLE_STORAGE

    def process_item(self, raw: dict) -> dict | None:
        required_fields = ["id", "slug", "name", "manufacturer"]
        for field in required_fields:
            if not raw.get(field):
                logger.warning("Storage item missing required field '%s': %s", field, raw.get("name", "?"))
                return None

        component = {
            "id": raw["id"],
            "slug": raw["slug"],
            "name": raw["name"],
            "type": "storage",
            "manufacturer": raw["manufacturer"],
            "description": raw.get("description", ""),
            "image": raw.get("image", ""),
            "releaseDate": raw.get("releaseDate", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            "msrp": float(raw.get("msrp", 0)),
            "prices": raw.get("prices", []),
            "specs": raw.get("specs", {}),
        }
        return component
