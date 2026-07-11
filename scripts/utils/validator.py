import json
import re
from pathlib import Path
from urllib.parse import urlparse

COMPONENT_SCHEMA = {
    "type": "object",
    "required": [
        "id", "slug", "name", "type", "manufacturer",
        "description", "image", "releaseDate", "msrp",
        "prices", "specs",
    ],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "slug": {"type": "string", "minLength": 1, "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$"},
        "name": {"type": "string", "minLength": 1},
        "type": {"type": "string", "enum": [
            "cpu", "gpu", "motherboard", "ram",
            "storage", "psu", "case", "cooler",
        ]},
        "manufacturer": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "image": {"type": "string"},
        "releaseDate": {"type": "string"},
        "msrp": {"type": "number", "minimum": 0},
        "prices": {"type": "array", "items": {"$ref": "#/$defs/PriceEntry"}},
        "specs": {"type": "object"},
        "gamingScore": {"type": "number"},
        "productivityScore": {"type": "number"},
        "aiScore": {"type": "number"},
    },
    "additionalProperties": False,
    "$defs": {
        "PriceEntry": {
            "type": "object",
            "required": ["retailer", "price", "url", "inStock", "lastChecked"],
            "properties": {
                "retailer": {"type": "string", "minLength": 1},
                "price": {"type": "number", "minimum": 0},
                "url": {"type": "string"},
                "inStock": {"type": "boolean"},
                "lastChecked": {"type": "string"},
            },
            "additionalProperties": False,
        },
    },
}

VALID_TYPES = {"cpu", "gpu", "motherboard", "ram", "storage", "psu", "case", "cooler"}

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_URL_SCHEMES = {"http", "https", ""}


def _is_valid_url(url: str) -> bool:
    if not url:
        return True
    try:
        parsed = urlparse(url)
        return parsed.scheme in _URL_SCHEMES and bool(parsed.netloc) or parsed.scheme == ""
    except Exception:
        return False


def _deep_validate(obj, schema, path=""):
    """Yield (path, message) tuples for every validation error found."""
    if "$defs" in schema:
        schema = {k: v for k, v in schema.items() if k != "$defs"}

    if "type" in schema:
        expected = schema["type"]
        actual = type(obj).__name__
        type_map = {
            "str": "string", "int": "number", "float": "number",
            "bool": "boolean", "list": "array", "dict": "object",
        }
        if expected == "number" and isinstance(obj, (int, float)):
            pass
        elif type_map.get(actual, actual) != expected:
            yield (path, f"Expected type '{expected}', got '{actual}'")
            return

    if "enum" in schema and obj not in schema["enum"]:
        yield (path, f"Value '{obj}' not in allowed values: {schema['enum']}")

    if "minLength" in schema and isinstance(obj, str) and len(obj) < schema["minLength"]:
        yield (path, f"String too short (min {schema['minLength']})")

    if "pattern" in schema and isinstance(obj, str) and not re.match(schema["pattern"], obj):
        yield (path, f"String does not match pattern '{schema['pattern']}'")

    if "minimum" in schema and isinstance(obj, (int, float)) and obj < schema["minimum"]:
        yield (path, f"Value {obj} is below minimum {schema['minimum']}")

    if schema.get("type") == "array" and isinstance(obj, list):
        items_schema = schema.get("items", {})
        for i, item in enumerate(obj):
            yield from _deep_validate(item, items_schema, f"{path}[{i}]")

    if schema.get("type") == "object" and isinstance(obj, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in obj:
                yield (path + ("." if path else "") + field, "Required field missing")

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, val in obj.items():
            if key in properties:
                yield from _deep_validate(val, properties[key], f"{path}.{key}")
            elif additional is False:
                yield (f"{path}.{key}", f"Unexpected property '{key}'")


def validate_component(component: dict, category: str) -> list[str]:
    errors = []
    if not isinstance(component, dict):
        return ["Component is not a dict"]

    for path, msg in _deep_validate(component, COMPONENT_SCHEMA):
        errors.append(f"{path}: {msg}")

    if "type" in component and component.get("type") != category.rstrip("s"):
        type_map = {
            "cpus": "cpu", "gpus": "gpu", "motherboards": "motherboard",
            "ram": "ram", "storage": "storage", "psus": "psu",
            "cases": "case", "coolers": "cooler",
        }
        expected = type_map.get(category, category)
        if component.get("type") != expected:
            errors.append(f"type: Expected '{expected}', got '{component.get('type')}'")

    if "image" in component and component["image"] and not _is_valid_url(component["image"]):
        errors.append("image: Invalid URL")

    for i, price_entry in enumerate(component.get("prices", [])):
        if "url" in price_entry and not _is_valid_url(price_entry["url"]):
            errors.append(f"prices[{i}].url: Invalid URL")

    if "slug" in component and not _SLUG_RE.match(component.get("slug", "")):
        errors.append("slug: Invalid slug format")

    return errors


def validate_file(filepath: str) -> dict:
    path = Path(filepath)
    result = {"valid": True, "errors": [], "warnings": [], "stats": {}}

    if not path.exists():
        result["valid"] = False
        result["errors"].append(f"File not found: {filepath}")
        return result

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result["valid"] = False
        result["errors"].append(f"Invalid JSON: {e}")
        return result

    if not isinstance(data, list):
        result["valid"] = False
        result["errors"].append("Root element is not an array")
        return result

    category = path.stem
    slugs = set()
    ids = set()
    total_errors = 0

    for i, component in enumerate(data):
        comp_errors = validate_component(component, category)

        slug = component.get("slug", "")
        if slug in slugs:
            comp_errors.append(f"Duplicate slug: '{slug}'")
        slugs.add(slug)

        comp_id = component.get("id", "")
        if comp_id in ids:
            comp_errors.append(f"Duplicate id: '{comp_id}'")
        ids.add(comp_id)

        for err in comp_errors:
            result["errors"].append(f"[{i}] {component.get('name', '?')}: {err}")
        total_errors += len(comp_errors)

    result["stats"] = {
        "total": len(data),
        "unique_slugs": len(slugs),
        "unique_ids": len(ids),
        "errors": total_errors,
    }

    if total_errors > 0:
        result["valid"] = False

    return result
