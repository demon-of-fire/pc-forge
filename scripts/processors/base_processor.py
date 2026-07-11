import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "public" / "data"


class BaseProcessor(ABC):
    """Base class for hardware data processors."""

    CATEGORY: str = ""

    @abstractmethod
    def fetch_data(self) -> list[dict]:
        """Fetch raw data from sources. Returns list of raw component dicts."""
        ...

    @abstractmethod
    def process_item(self, raw: dict) -> dict | None:
        """Process a single raw item into a Component dict. Returns None to skip."""
        ...

    def process_all(self) -> list[dict]:
        """Fetch and process all items. Handles errors gracefully."""
        logger.info("Starting processing for category: %s", self.CATEGORY)
        try:
            raw_items = self.fetch_data()
        except Exception as e:
            logger.error("Failed to fetch data for %s: %s", self.CATEGORY, e)
            return []

        logger.info("Fetched %d raw items for %s", len(raw_items), self.CATEGORY)
        processed = []
        skipped = 0
        for item in raw_items:
            try:
                result = self.process_item(item)
                if result is not None:
                    processed.append(result)
                else:
                    skipped += 1
            except Exception as e:
                logger.warning("Failed to process item %s: %s", item.get("name", "?"), e)
                skipped += 1

        logger.info(
            "Processed %d items, skipped %d for %s",
            len(processed), skipped, self.CATEGORY,
        )
        return processed

    def get_existing_slugs(self, data_path: str | Path) -> set[str]:
        """Load existing data and return set of slugs for dedup."""
        path = Path(data_path)
        if not path.exists():
            return set()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {item.get("slug", "") for item in data if isinstance(item, dict)}
        except Exception as e:
            logger.error("Failed to load existing data from %s: %s", path, e)
            return set()

    def save(self, components: list[dict], data_path: str | Path):
        """Save processed components to JSON file."""
        path = Path(data_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(components, f, indent=2, ensure_ascii=False)
        logger.info("Saved %d components to %s", len(components), path)
