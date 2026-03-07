from loguru import logger
from scraper.browser import Browser
from scraper.parser import parse_apartment
import random
import time


def scrape_apartments(urls, headless=True, timeout=30000):
    """
    Scrape apartment data from given URLs.
    
    Args:
        urls: List of apartment listing URLs
        headless: Run browser in headless mode
        timeout: Page load timeout in milliseconds
        
    Returns:
        List of apartment data dictionaries
    """
    apartments = []
    
    with Browser(headless=headless, timeout=timeout) as context:
        page = context.new_page()
        
        for i, url in enumerate(urls, 1):
            try:
                # Random delay between requests (2-5 seconds)
                if i > 1:
                    delay = random.uniform(2, 5)
                    logger.debug(f"Waiting {delay:.1f}s before next request...")
                    time.sleep(delay)
                
                logger.info(f"Scraping {i}/{len(urls)}")
                page.goto(url, wait_until='networkidle')
                
                # Random delay after page load (1-3 seconds)
                time.sleep(random.uniform(1, 3))
                
                html = page.content()
                apartment = parse_apartment(html, url)
                
                if apartment:
                    apartments.append(apartment)
                
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                continue
    
    logger.success(f"Scraped {len(apartments)}/{len(urls)} apartments")
    return apartments
