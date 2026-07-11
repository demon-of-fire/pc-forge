import re
from difflib import SequenceMatcher


def _normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_duplicates(components: list[dict]) -> list[tuple[dict, dict]]:
    pairs = []
    seen = set()

    slug_map: dict[str, list[dict]] = {}
    for comp in components:
        slug = comp.get("slug", "")
        slug_map.setdefault(slug, []).append(comp)

    for slug, group in slug_map.items():
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    key = (id(group[i]), id(group[j]))
                    if key not in seen:
                        seen.add(key)
                        pairs.append((group[i], group[j]))

    names = [(comp, _normalize_name(comp.get("name", ""))) for comp in components]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            comp_a, norm_a = names[i]
            comp_b, norm_b = names[j]
            key = (id(comp_a), id(comp_b))
            if key in seen:
                continue
            if norm_a == norm_b or _similarity(norm_a, norm_b) > 0.9:
                seen.add(key)
                pairs.append((comp_a, comp_b))

    return pairs


def merge_duplicates(primary: dict, secondary: dict) -> dict:
    merged = dict(primary)

    for key in ("description", "image", "releaseDate", "msrp"):
        if not merged.get(key) and secondary.get(key):
            merged[key] = secondary[key]

    if not merged.get("gamingScore") and secondary.get("gamingScore"):
        merged["gamingScore"] = secondary["gamingScore"]
    if not merged.get("productivityScore") and secondary.get("productivityScore"):
        merged["productivityScore"] = secondary["productivityScore"]
    if not merged.get("aiScore") and secondary.get("aiScore"):
        merged["aiScore"] = secondary["aiScore"]

    primary_retailers = {p["retailer"] for p in merged.get("prices", [])}
    for price in secondary.get("prices", []):
        if price["retailer"] not in primary_retailers:
            merged.setdefault("prices", []).append(price)
            primary_retailers.add(price["retailer"])

    primary_specs = set(merged.get("specs", {}).keys())
    for k, v in secondary.get("specs", {}).items():
        if k not in primary_specs:
            merged.setdefault("specs", {})[k] = v

    return merged
