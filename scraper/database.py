"""SQLite storage for apartment data."""
import json
import sqlite3
from loguru import logger

DB_PATH = "data/apartments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS apartments (
    id TEXT PRIMARY KEY,
    url TEXT,
    description TEXT,
    price REAL,
    living_area REAL,
    rooms REAL,
    floor TEXT,
    district TEXT,
    city TEXT,
    postal_code TEXT,
    coordinates TEXT,
    building_type TEXT,
    building_condition TEXT,
    heating TEXT,
    energy_hwb TEXT,
    energy_hwb_class TEXT,
    ownership_type TEXT,
    is_private INTEGER,
    created_date TEXT,
    published_date TEXT,
    scraped_batch TEXT,
    raw_data TEXT
);
"""


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(SCHEMA)
    return conn


def _parse_number(value):
    """Parse German-format numbers like '57,51' to float."""
    if not value:
        return None
    try:
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None


def _extract_fields(apt):
    """Extract indexed fields from apartment dict."""
    addr = apt.get("advertAddressDetails", {})
    return {
        "id": apt.get("id"),
        "url": apt.get("url"),
        "description": apt.get("description"),
        "price": _parse_number(apt.get("PRICE")),
        "living_area": _parse_number(apt.get("ESTATE_SIZE/LIVING_AREA")),
        "rooms": _parse_number(apt.get("NO_OF_ROOMS")),
        "floor": apt.get("FLOOR"),
        "district": apt.get("LOCATION/ADDRESS_2"),
        "city": apt.get("LOCATION/ADDRESS_3"),
        "postal_code": addr.get("postalCode") if isinstance(addr, dict) else None,
        "coordinates": apt.get("COORDINATES"),
        "building_type": apt.get("BUILDING_TYPE"),
        "building_condition": apt.get("BUILDING_CONDITION"),
        "heating": apt.get("HEATING") if isinstance(apt.get("HEATING"), str) else None,
        "energy_hwb": apt.get("ENERGY_HWB"),
        "energy_hwb_class": apt.get("ENERGY_HWB_CLASS"),
        "ownership_type": apt.get("OWNAGETYPE"),
        "is_private": int(apt.get("ISPRIVATE", 0)),
        "created_date": apt.get("createdDate"),
        "published_date": apt.get("publishedDate"),
        "scraped_batch": apt.get("scraped_batch"),
        "raw_data": json.dumps(apt, ensure_ascii=False),
    }


def save_apartments(apartments):
    """Save apartments to SQLite. Skips duplicates by URL."""
    conn = _connect()
    fields = list(_extract_fields({}).keys())
    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)

    inserted = 0
    for apt in apartments:
        row = _extract_fields(apt)
        try:
            conn.execute(
                f"INSERT OR REPLACE INTO apartments ({columns}) VALUES ({placeholders})",
                [row[f] for f in fields],
            )
            inserted += conn.total_changes  # approximate
        except Exception as e:
            logger.warning(f"Failed to insert {apt.get('url')}: {e}")

    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM apartments").fetchone()[0]
    conn.close()
    logger.success(f"Saved to SQLite. Total: {total} apartments")
    return total


def load_apartments():
    """Load all apartments as list of dicts (from raw_data)."""
    conn = _connect()
    rows = conn.execute("SELECT raw_data FROM apartments").fetchall()
    conn.close()
    return [json.loads(r[0]) for r in rows]


def count_apartments():
    conn = _connect()
    count = conn.execute("SELECT COUNT(*) FROM apartments").fetchone()[0]
    conn.close()
    return count


def get_existing_ids():
    """Get set of all scraped apartment IDs."""
    conn = _connect()
    rows = conn.execute("SELECT id FROM apartments").fetchall()
    conn.close()
    return {r[0] for r in rows}
