"""
Scrape apartments from the first page in queue.
Run this periodically (e.g. every hour) to process one page at a time.
"""
import json
import os
from datetime import datetime
from loguru import logger
from scraper.browser import Browser
from scraper.parser import extract_search_results
from scraper.scraper import scrape_apartments
from config import HEADLESS, TIMEOUT


def load_queue():
    """Load pages queue"""
    queue_file = "data/pages_queue.json"
    
    if not os.path.exists(queue_file):
        logger.warning("Queue file not found. Run collect_pages.py first.")
        return []
    
    with open(queue_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_queue(queue):
    """Save updated queue"""
    queue_file = "data/pages_queue.json"
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def load_existing_apartments():
    """Load existing apartments data"""
    apartments_file = "data/apartments.json"
    
    if not os.path.exists(apartments_file):
        return []
    
    with open(apartments_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_apartments(apartments):
    """Save apartments data"""
    apartments_file = "data/apartments.json"
    with open(apartments_file, 'w', encoding='utf-8') as f:
        json.dump(apartments, f, ensure_ascii=False, indent=2)


def main():
    logger.info("Starting page scraper")
    
    os.makedirs("data", exist_ok=True)
    
    # Load queue
    queue = load_queue()
    
    if not queue:
        logger.warning("Queue is empty. Nothing to scrape.")
        return
    
    # Get first page URL
    page_url = queue[0]
    logger.info(f"Processing page 1/{len(queue)}: {page_url}")
    
    # Scrape apartment URLs from this page
    with Browser(headless=HEADLESS, timeout=TIMEOUT) as context:
        page = context.new_page()
        page.goto(page_url)
        page.wait_for_load_state("networkidle")
        
        html = page.content()
        apartment_urls = extract_search_results(html, max_results=None)  # Get all from page
    
    if not apartment_urls:
        logger.error("No apartments found on this page")
        # Remove page from queue anyway
        queue.pop(0)
        save_queue(queue)
        return
    
    logger.info(f"Found {len(apartment_urls)} apartments on this page")
    
    # Scrape all apartments from this page
    apartments = scrape_apartments(apartment_urls, headless=HEADLESS, timeout=TIMEOUT)
    
    # Load existing apartments and merge
    existing_apartments = load_existing_apartments()
    
    # Add scraped_batch timestamp
    batch_time = datetime.now().isoformat()
    for apt in apartments:
        apt['scraped_batch'] = batch_time
    
    # Merge (avoid duplicates by URL)
    existing_urls = {apt['url'] for apt in existing_apartments}
    new_apartments = [apt for apt in apartments if apt['url'] not in existing_urls]
    
    updated_apartments = existing_apartments + new_apartments
    
    # Save updated apartments
    save_apartments(updated_apartments)
    
    logger.success(f"Added {len(new_apartments)} new apartments (total: {len(updated_apartments)})")
    
    # Remove processed page from queue
    queue.pop(0)
    save_queue(queue)
    
    logger.success(f"Page processed. {len(queue)} pages remaining in queue")


if __name__ == "__main__":
    main()
