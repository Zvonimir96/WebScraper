#!/home/zvone/proj/webScraper/venv/bin/python
"""Import existing apartments.json into SQLite database."""
import json
import os
from loguru import logger
from scraper.database import save_apartments, count_apartments

JSON_FILE = "data/apartments.json"


def main():
    if not os.path.exists(JSON_FILE):
        logger.error(f"{JSON_FILE} not found")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        apartments = json.load(f)

    logger.info(f"Importing {len(apartments)} apartments from JSON to SQLite...")
    save_apartments(apartments)
    logger.success(f"Done. {count_apartments()} apartments in database.")


if __name__ == "__main__":
    main()
