#!/usr/bin/env python3
"""Daily incremental update for PCForge hardware database."""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "public" / "data"
STATE_DIR = SCRIPTS_DIR / "state"
STATE_FILE = STATE_DIR / "progress.json"

sys.path.insert(0, str(SCRIPTS_DIR))

from processors.cpu_processor import CPUProcessor
from processors.gpu_processor import GPUProcessor
from processors.motherboard_processor import MotherboardProcessor
from processors.ram_processor import RAMProcessor
from processors.storage_processor import StorageProcessor
from processors.psu_processor import PSUProcessor
from processors.case_processor import CaseProcessor
from processors.cooler_processor import CoolerProcessor
from utils.validator import validate_file
from utils.deduplicator import find_duplicates, merge_duplicates
from utils.reporter import generate_report

logger = logging.getLogger("daily_update")

PROCESSORS = {
    "cpus": CPUProcessor,
    "gpus": GPUProcessor,
    "motherboards": MotherboardProcessor,
    "ram": RAMProcessor,
    "storage": StorageProcessor,
    "psus": PSUProcessor,
    "cases": CaseProcessor,
    "coolers": CoolerProcessor,
}


def load_existing_data(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to load %s: %s", filepath, e)
        return []


def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_run": None,
        "last_success": None,
        "runs": [],
        "stats": {"total_components": 0, "categories": {}},
    }


def save_state(state: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def diff_categories(
    existing: list[dict], new: list[dict], category: str
) -> tuple[list[dict], dict]:
    existing_by_slug = {item["slug"]: item for item in existing if "slug" in item}
    new_by_slug = {item["slug"]: item for item in new if "slug" in item}

    added = []
    updated = []
    removed = []

    for slug, item in new_by_slug.items():
        if slug not in existing_by_slug:
            added.append(item)
        else:
            existing_item = existing_by_slug[slug]
            changed_fields = []
            for key in set(list(item.keys()) + list(existing_item.keys())):
                if key == "prices":
                    continue
                old_val = existing_item.get(key)
                new_val = item.get(key)
                if old_val != new_val:
                    changed_fields.append(key)
            if changed_fields:
                updated.append((slug, changed_fields))

    for slug in existing_by_slug:
        if slug not in new_by_slug:
            removed.append(slug)

    changes = {
        "added": added,
        "updated": updated,
        "removed": removed,
    }

    return new, changes


def deduplicate_category(components: list[dict], category: str) -> list[dict]:
    pairs = find_duplicates(components)
    if not pairs:
        return components

    logger.info("Found %d duplicate pairs in %s", len(pairs), category)
    to_remove = set()

    for primary, secondary in pairs:
        if id(secondary) in to_remove:
            continue
        merged = merge_duplicates(primary, secondary)
        idx_p = components.index(primary)
        components[idx_p] = merged
        to_remove.add(id(secondary))

    deduplicated = [c for c in components if id(c) not in to_remove]
    return deduplicated


def run_update(
    category_filter: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
):
    categories_to_run = list(PROCESSORS.keys())
    if category_filter:
        if category_filter not in PROCESSORS:
            logger.error("Unknown category: %s (valid: %s)", category_filter, ", ".join(PROCESSORS.keys()))
            return
        categories_to_run = [category_filter]

    state = load_state()
    run_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "categories": {},
        "dry_run": dry_run,
    }

    all_stats = {}
    all_changes = {"added": {}, "removed": {}, "updated": {}}

    for category in categories_to_run:
        logger.info("=== Updating category: %s ===", category)
        processor_cls = PROCESSORS[category]
        processor = processor_cls()

        data_file = DATA_DIR / f"{category}.json"
        existing = load_existing_data(data_file)

        new_data = processor.process_all()
        new_data = deduplicate_category(new_data, category)

        merged, category_changes = diff_categories(existing, new_data, category)

        added_count = len(category_changes["added"])
        updated_count = len(category_changes["updated"])
        removed_count = len(category_changes["removed"])

        logger.info(
            "%s: +%d added, ~%d updated, -%d removed",
            category, added_count, updated_count, removed_count,
        )

        all_changes["added"][category] = category_changes["added"]
        all_changes["removed"][category] = category_changes["removed"]
        all_changes["updated"][category] = category_changes["updated"]

        if not dry_run:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            processor.save(merged, data_file)

            validation = validate_file(str(data_file))
            all_stats[category] = validation["stats"]
            if not validation["valid"]:
                logger.warning("Validation issues for %s: %d errors", category, len(validation["errors"]))
        else:
            logger.info("[DRY RUN] Would save %d items to %s", len(merged), data_file)

        run_record["categories"][category] = {
            "existing": len(existing),
            "new": len(merged),
            "added": added_count,
            "updated": updated_count,
            "removed": removed_count,
            "status": "success",
        }

    if not dry_run:
        state["last_run"] = run_record["timestamp"]
        state["last_success"] = run_record["timestamp"]
        state["runs"].append(run_record)
        if len(state["runs"]) > 30:
            state["runs"] = state["runs"][-30:]

        total = sum(all_stats.get(c, {}).get("total", 0) for c in categories_to_run)
        state["stats"]["total_components"] = total
        for cat in categories_to_run:
            state["stats"]["categories"][cat] = all_stats.get(cat, {})

        save_state(state)

    report = generate_report(all_stats, all_changes)
    report_path = STATE_DIR / "last_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info("Report saved to %s", report_path)

    if verbose:
        print(report)

    return report


def main():
    parser = argparse.ArgumentParser(description="PCForge: Daily incremental update")
    parser.add_argument(
        "--category", "-c",
        choices=list(PROCESSORS.keys()),
        help="Run only a specific category",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview changes without saving",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print the report to stdout",
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    run_update(
        category_filter=args.category,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
