#!/usr/bin/env python3
"""
Local scraping script for PCForge hardware data.

Run this from your local machine (residential IP) to scrape real prices
from PCPartPicker. PCPartPicker blocks cloud/datacenter IPs, so this
must be run locally.

Usage:
    py scripts/local_scrape.py                    # Scrape all categories
    py scripts/local_scrape.py --category cpus    # Scrape only CPUs
    py scripts/local_scrape.py --commit           # Auto-commit changes
    py scripts/local_scrape.py --dry-run          # Preview without saving
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "public" / "data"

sys.path.insert(0, str(SCRIPTS_DIR))

from scrapers.pcpartpicker import scrape_product_list, match_to_existing
from processors.cpu_processor import CPUProcessor
from processors.gpu_processor import GPUProcessor
from processors.motherboard_processor import MotherboardProcessor
from processors.ram_processor import RAMProcessor
from processors.storage_processor import StorageProcessor
from processors.psu_processor import PSUProcessor
from processors.case_processor import CaseProcessor
from processors.cooler_processor import CoolerProcessor
from utils.validator import validate_file

logger = logging.getLogger("local_scrape")

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


def load_existing(category: str) -> list[dict]:
    path = DATA_DIR / f"{category}.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(category: str, data: list[dict]):
    path = DATA_DIR / f"{category}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info("Saved %d items to %s", len(data), path)


def scrape_category(category: str, dry_run: bool = False) -> dict:
    """Scrape one category from PCPartPicker and merge with existing data."""
    existing = load_existing(category)
    logger.info("Existing %s: %d items", category, len(existing))

    logger.info("Scraping %s from PCPartPicker...", category)
    scraped = scrape_product_list(category, max_pages=5)

    if not scraped:
        logger.warning("No products scraped for %s — keeping existing data", category)
        return {"scraped": 0, "new": 0, "updated": 0, "total": len(existing)}

    updated, new_prods = match_to_existing(scraped, existing)
    merged = updated + new_prods

    logger.info(
        "Scraped %d, matched %d existing, found %d new — total: %d",
        len(scraped), len(updated), len(new_prods), len(merged),
    )

    if not dry_run and merged:
        save_data(category, merged)

    return {
        "scraped": len(scraped),
        "new": len(new_prods),
        "updated": len(updated),
        "total": len(merged),
    }


def commit_changes(categories: list[str]):
    """Git add and commit the updated data files."""
    try:
        subprocess.run(["git", "add", "public/data/*.json"], cwd=PROJECT_ROOT, check=True)
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=PROJECT_ROOT, capture_output=True,
        )
        if result.returncode == 0:
            logger.info("No changes to commit")
            return

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        msg = f"chore: update hardware prices ({', '.join(categories)}) — {now}"
        subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT_ROOT, check=True)
        logger.info("Committed: %s", msg)

        subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
        logger.info("Pushed to remote")
    except subprocess.CalledProcessError as e:
        logger.error("Git operation failed: %s", e)


def main():
    parser = argparse.ArgumentParser(description="Scrape PCPartPicker from local machine")
    parser.add_argument("--category", "-c", choices=list(PROCESSORS.keys()), help="Single category")
    parser.add_argument("--commit", action="store_true", help="Auto-commit and push changes")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview without saving")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    categories = [args.category] if args.category else list(PROCESSORS.keys())
    results = {}

    for cat in categories:
        logger.info("=== %s ===", cat.upper())
        try:
            results[cat] = scrape_category(cat, dry_run=args.dry_run)
        except Exception as e:
            logger.error("Failed to scrape %s: %s", cat, e)
            results[cat] = {"error": str(e)}

    # Summary
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)
    for cat, r in results.items():
        if "error" in r:
            print(f"  {cat}: ERROR — {r['error']}")
        else:
            print(f"  {cat}: scraped={r['scraped']}, new={r['new']}, updated={r['updated']}, total={r['total']}")
    print("=" * 60)

    if args.commit and not args.dry_run:
        commit_changes(categories)


if __name__ == "__main__":
    main()
