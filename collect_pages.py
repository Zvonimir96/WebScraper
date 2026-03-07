"""
Collect all search result page URLs and save to queue.
Run this periodically (e.g. every hour) to refresh the queue.
"""
import json
import os
from loguru import logger
from scraper.browser import Browser, open_search_page
from config import SEARCH_CONFIG, HEADLESS, TIMEOUT


def collect_page_urls():
    """
    Collect all search result page URLs
    
    Returns:
        List of page URLs
    """
    page_urls = []
    
    with Browser(headless=HEADLESS, timeout=TIMEOUT) as context:
        page = context.new_page()
        
        # Open first page
        open_search_page(
            page,
            city=SEARCH_CONFIG['city'],
            property_type=SEARCH_CONFIG['property_type'],
            price_max=SEARCH_CONFIG.get('price_max'),
            area_min=SEARCH_CONFIG.get('area_min')
        )
        
        # Get current URL (page 1)
        base_url = page.url.split('&page=')[0]
        
        # Extract total pages from JSON
        html = page.content()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        script = soup.find('script', {'id': '__NEXT_DATA__'})
        
        if script:
            data = json.loads(script.string)
            page_props = data['props']['pageProps']
            
            if 'searchResult' in page_props:
                search_result = page_props['searchResult']
            elif 'initialSearchResult' in page_props:
                search_result = page_props['initialSearchResult']
            else:
                logger.error("No search results found")
                return []
            
            total_rows = search_result.get('rowsFound', 0)
            rows_per_page = search_result.get('rowsReturned', 30)
            total_pages = (total_rows + rows_per_page - 1) // rows_per_page
            
            logger.info(f"Found {total_rows} apartments across {total_pages} pages")
            
            # Generate page URLs
            for page_num in range(1, total_pages + 1):
                if page_num == 1:
                    page_url = base_url
                else:
                    page_url = f"{base_url}&page={page_num}"
                page_urls.append(page_url)
    
    return page_urls


def main():
    logger.info("Starting page collection")
    
    os.makedirs("data", exist_ok=True)
    
    # Collect all page URLs
    page_urls = collect_page_urls()
    
    if not page_urls:
        logger.error("No pages found")
        return
    
    # Save to queue file
    queue_file = "data/pages_queue.json"
    
    # Load existing queue if exists
    existing_queue = []
    if os.path.exists(queue_file):
        with open(queue_file, 'r', encoding='utf-8') as f:
            existing_queue = json.load(f)
        logger.info(f"Loaded {len(existing_queue)} existing pages from queue")
    
    # Add new pages (avoid duplicates)
    new_pages = [url for url in page_urls if url not in existing_queue]
    updated_queue = existing_queue + new_pages
    
    # Save updated queue
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(updated_queue, f, ensure_ascii=False, indent=2)
    
    logger.success(f"Queue updated: {len(existing_queue)} existing + {len(new_pages)} new = {len(updated_queue)} total pages")


if __name__ == "__main__":
    main()
