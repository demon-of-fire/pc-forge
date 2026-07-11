"""Shared web scraping utilities for PCForge hardware data collection."""

import logging
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_session: requests.Session | None = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
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


def fetch_page(url: str) -> BeautifulSoup | None:
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)

    try:
        session = get_session()
        resp = session.get(url, timeout=30)
        LAST_REQUEST_TIME = time.time()
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except requests.RequestException as e:
        logger.warning("Failed to fetch %s: %s", url, e)
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
