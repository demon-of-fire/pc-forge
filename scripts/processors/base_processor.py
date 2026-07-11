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
    def seed_data(self) -> list[dict]:
        """Return hardcoded seed data as fallback."""
        ...

    def process_item(self, raw: dict) -> dict | None:
        """Process a single raw item into a Component dict. Returns None to skip."""
        return raw

    def update_existing(self, category: str) -> list[dict] | None:
        """Attempt to scrape live data. Returns merged data or None if nothing new.
        
        Used by daily_update — if scraping fails, returns None so the
        existing JSON file is NOT overwritten.
        """
        logger.info("Attempting live scrape for category: %s", self.CATEGORY)
        try:
            raw_items = self.fetch_data()
            if raw_items and len(raw_items) >= 3:
                logger.info("Fetched %d live items for %s", len(raw_items), self.CATEGORY)
                processed = []
                for item in raw_items:
                    try:
                        result = self.process_item(item)
                        if result is not None:
                            processed.append(result)
                    except Exception as e:
                        logger.warning("Failed to process item %s: %s", item.get("name", "?"), e)
                if processed:
                    return processed
            logger.warning("Live scrape returned insufficient data for %s — keeping existing", self.CATEGORY)
            return None
        except Exception as e:
            logger.error("Live scrape failed for %s: %s — keeping existing", self.CATEGORY, e)
            return None

    def process_all(self) -> list[dict]:
        """Fetch and process all items. Falls back to seed data on failure."""
        logger.info("Starting processing for category: %s", self.CATEGORY)
        try:
            raw_items = self.fetch_data()
            if raw_items and len(raw_items) >= 3:
                logger.info("Fetched %d live items for %s", len(raw_items), self.CATEGORY)
            else:
                logger.warning(
                    "Scraping returned %d items for %s (minimum 3 required), using seed data",
                    len(raw_items) if raw_items else 0, self.CATEGORY,
                )
                raw_items = self.seed_data()
        except Exception as e:
            logger.error("Scraping failed for %s: %s — using seed data", self.CATEGORY, e)
            raw_items = self.seed_data()

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

        logger.info("Processed %d items, skipped %d for %s", len(processed), skipped, self.CATEGORY)
        return processed

    def merge_with_existing(self, new_data: list[dict], data_path: Path) -> list[dict]:
        """Merge new scraped data with existing data, preserving existing specs."""
        existing = self._load_existing(data_path)
        if not existing:
            return new_data

        existing_map = {item.get("slug", ""): item for item in existing}
        merged = []
        seen_slugs = set()

        for item in new_data:
            slug = item.get("slug", "")
            if slug in existing_map:
                merged_item = self._merge_items(existing_map[slug], item)
                merged.append(merged_item)
            else:
                merged.append(item)
            seen_slugs.add(slug)

        for slug, item in existing_map.items():
            if slug not in seen_slugs:
                merged.append(item)

        return merged

    def _merge_items(self, existing: dict, new: dict) -> dict:
        """Merge two items, preferring existing for specs, new for prices."""
        merged = dict(existing)
        if new.get("prices"):
            merged["prices"] = new["prices"]
        for key in new:
            if key not in merged or merged[key] is None or merged[key] == "" or merged[key] == 0:
                merged[key] = new[key]
        return merged

    def _load_existing(self, data_path: Path) -> list[dict]:
        if not data_path.exists():
            return []
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error("Failed to load existing data from %s: %s", data_path, e)
            return []

    def save(self, components: list[dict], data_path: str | Path):
        path = Path(data_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(components, f, indent=2, ensure_ascii=False)
        logger.info("Saved %d components to %s", len(components), path)
