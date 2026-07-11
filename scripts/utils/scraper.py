"""Shared web scraping utilities for PCForge hardware data collection.

Uses Playwright (headless Chromium) as primary engine to bypass Cloudflare,
with requests as fallback for sites that don't need JS rendering.
"""

import logging
import os
import re
import time
from contextlib import contextmanager

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

LAST_REQUEST_TIME = 0.0
REQUEST_DELAY = 2.5

_playwright_browser = None
_playwright_context = None


def _get_playwright_browser():
    """Lazily initialize Playwright browser (shared across requests)."""
    global _playwright_browser, _playwright_context
    if _playwright_browser is not None:
        return _playwright_browser, _playwright_context

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("playwright not installed — pip install playwright && playwright install chromium")
        return None, None

    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-GB",
        timezone_id="Europe/London",
    )
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-GB', 'en'] });
        window.chrome = { runtime: {} };
    """)
    _playwright_browser = browser
    _playwright_context = context
    return browser, context


def close_playwright():
    """Clean up Playwright resources."""
    global _playwright_browser, _playwright_context
    if _playwright_context:
        _playwright_context.close()
        _playwright_context = None
    if _playwright_browser:
        _playwright_browser.close()
        _playwright_browser = None


def fetch_page(url: str) -> BeautifulSoup | None:
    """Fetch a page using Playwright (primary) with requests fallback."""
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)

    result = _fetch_with_playwright(url)
    if result:
        return result

    logger.info("Playwright failed, trying requests for %s", url)
    return _fetch_with_requests(url)


def _is_challenge_or_blocked(html: str, title: str) -> bool:
    """Check if the page is a Cloudflare challenge or blocked page."""
    if title in ("Unavailable", "Just a moment"):
        return True
    if "Just a moment" in html[:2000]:
        return True
    if "PCPartPicker is unavailable" in html:
        return True
    return False


def _fetch_with_playwright(url: str) -> BeautifulSoup | None:
    """Fetch page content using Playwright headless browser."""
    browser, context = _get_playwright_browser()
    if browser is None or context is None:
        return None

    page = None
    try:
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        for _ in range(20):
            title = page.title()
            html = page.content()
            if not _is_challenge_or_blocked(html, title):
                break
            logger.info("Waiting for Cloudflare challenge to resolve...")
            page.wait_for_timeout(2000)
        else:
            logger.warning("Cloudflare challenge did not resolve for %s", url)
            return None

        page.wait_for_timeout(1500)
        html = page.content()
        global LAST_REQUEST_TIME
        LAST_REQUEST_TIME = time.time()
        return BeautifulSoup(html, "lxml")
    except Exception as e:
        logger.warning("Playwright failed for %s: %s", url, e)
        return None
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass


def _fetch_with_requests(url: str) -> BeautifulSoup | None:
    """Fallback: fetch page using plain requests."""
    import requests as req

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    }
    for attempt in range(2):
        try:
            resp = req.get(url, headers=headers, timeout=30)
            global LAST_REQUEST_TIME
            LAST_REQUEST_TIME = time.time()
            if resp.status_code == 403:
                logger.warning("Requests got 403 for %s", url)
                return None
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            logger.warning("Requests failed for %s: %s", url, e)
            time.sleep(2)
    return None


def make_slug(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def make_id(category: str, slug: str) -> str:
    cat = category.rstrip("s")
    return f"{cat}-{slug}"


def guess_manufacturer(name: str) -> str:
    lower = name.lower()
    manufacturers = [
        ("amd", "AMD"), ("intel", "Intel"), ("nvidia", "NVIDIA"),
        ("geforce", "NVIDIA"), ("radeon", "AMD"),
        ("corsair", "Corsair"), ("crucial", "Crucial"),
        ("samsung", "Samsung"), ("western digital", "Western Digital"),
        ("wd", "Western Digital"), ("seagate", "Seagate"),
        ("kingston", "Kingston"), ("g.skill", "G.Skill"),
        ("skill", "G.Skill"), ("teamgroup", "TeamGroup"),
        ("be quiet", "be quiet!"), ("noctua", "Noctua"),
        ("arctic", "Arctic"), ("deepcool", "DeepCool"),
        ("nzxt", "NZXT"), ("lian li", "Lian Li"),
        ("fractal", "Fractal Design"), ("phanteks", "Phanteks"),
        ("cooler master", "Cooler Master"), ("thermaltake", "Thermaltake"),
        ("evga", "EVGA"), ("msi", "MSI"), ("asus", "ASUS"),
        ("gigabyte", "Gigabyte"), ("asrock", "ASRock"),
        ("zotac", "Zotac"), ("palit", "Palit"),
        ("seasonic", "Seasonic"), ("evga", "EVGA"),
        ("silverstone", "SilverStone"), ("super flower", "Super Flower"),
        ("adata", "ADATA"), ("pny", "PNY"),
        ("intel core", "Intel"), ("ryzen", "AMD"),
    ]
    for key, mfr in manufacturers:
        if key in lower:
            return mfr
    return name.split()[0] if name else "Unknown"


def generate_description(name: str, specs: dict) -> str:
    parts = []
    if "cores" in specs and "threads" in specs:
        parts.append(f"{specs['cores']}-core, {specs['threads']}-thread")
    elif "cores" in specs:
        parts.append(f"{specs['cores']}-core")
    if "architecture" in specs:
        parts.append(str(specs["architecture"]))
    if "socket" in specs:
        parts.append(f"{specs['socket']} socket")
    if parts:
        return f"{name} — {' '.join(parts)} processor."
    return f"{name} — high-performance PC component."
