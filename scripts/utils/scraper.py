"""Shared web scraping utilities for PCForge hardware data collection."""

import logging
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_session: requests.Session | None = None
_cloudscraper_session = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24", "Google Chrome";v="137"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

LAST_REQUEST_TIME = 0.0
REQUEST_DELAY = 2.0


def get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(HEADERS)
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
            )
        )
        _session.mount("https://", adapter)
        _session.mount("http://", adapter)
    return _session


def get_cloudscraper_session():
    global _cloudscraper_session
    if _cloudscraper_session is None:
        try:
            import cloudscraper
            _cloudscraper_session = cloudscraper.create_scraper(
                browser={"browser": "chrome", "platform": "windows", "desktop": True}
            )
            _cloudscraper_session.headers.update(HEADERS)
        except ImportError:
            logger.warning("cloudscraper not installed, falling back to requests")
            return None
    return _cloudscraper_session


def fetch_page(url: str) -> BeautifulSoup | None:
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)

    for attempt in range(3):
        try:
            session = get_session()
            if attempt > 0:
                session.headers["Referer"] = "https://uk.pcpartpicker.com/"
            resp = session.get(url, timeout=30)
            LAST_REQUEST_TIME = time.time()

            if resp.status_code == 403:
                logger.info("Got 403 from requests, trying cloudscraper for %s", url)
                result = _try_cloudscraper(url)
                if result:
                    return result

            resp.raise_for_status()

            text = resp.text
            if "challenge-platform" in text or "Just a moment" in text:
                logger.warning("Cloudflare challenge detected for %s (attempt %d)", url, attempt + 1)
                result = _try_cloudscraper(url)
                if result:
                    return result
                time.sleep(5 * (attempt + 1))
                continue

            return BeautifulSoup(text, "lxml")
        except requests.RequestException as e:
            logger.warning("Failed to fetch %s (attempt %d): %s", url, attempt + 1, e)
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
    return None


def _try_cloudscraper(url: str) -> BeautifulSoup | None:
    """Attempt to fetch using cloudscraper to bypass Cloudflare."""
    cs = get_cloudscraper_session()
    if cs is None:
        return None
    try:
        logger.info("Fetching %s via cloudscraper", url)
        resp = cs.get(url, timeout=30)
        resp.raise_for_status()
        text = resp.text
        if "challenge-platform" in text or "Just a moment" in text:
            logger.warning("Cloudflare challenge still present after cloudscraper for %s", url)
            return None
        return BeautifulSoup(text, "lxml")
    except Exception as e:
        logger.warning("cloudscraper failed for %s: %s", url, e)
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
