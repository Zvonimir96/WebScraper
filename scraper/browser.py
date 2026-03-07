from playwright.sync_api import sync_playwright
from loguru import logger
import random
import time


class Browser:
    def __init__(self, headless=True, timeout=30000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser = None
        self.context = None
        
    def __enter__(self):
        self.playwright = sync_playwright().start()
        
        # Launch with stealth settings
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        # Create context with realistic settings
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='de-AT',
            timezone_id='Europe/Vienna',
        )
        
        self.context.set_default_timeout(self.timeout)
        logger.info("Browser started")
        return self.context
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser closed")


def open_search_page(page, city, property_type, price_max=None, area_min=None):
    """
    Open willhaben.at and fill search form
    
    Args:
        page: Playwright page object
        city: City name (e.g. "Graz")
        property_type: Property type value (101 = Wohnung kaufen, 102 = Wohnung mieten)
        price_max: Maximum price (optional)
        area_min: Minimum living area in m² (optional)
    
    Returns:
        Page object with search results loaded
    """
    # Map city to areaId (Graz = 60101)
    city_area_map = {
        'Graz': '60101',
        'Wien': '900',
        'Linz': '40101',
        'Salzburg': '50101',
        'Innsbruck': '70101',
    }
    
    area_id = city_area_map.get(city)
    if not area_id:
        logger.warning(f"Unknown city: {city}, using form method")
        # Fallback to form method
        page.goto("https://www.willhaben.at/iad/immobilien/")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector('select#searchid-select', state='visible')
        page.select_option('select#searchid-select', property_type)
        page.fill('input#location-autocomplete-input', city)
        page.wait_for_timeout(1500)
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)
    else:
        # Direct URL method (more reliable)
        logger.info(f"Opening search for {city} (areaId={area_id})")
        
        # Build URL based on property type
        if property_type == "101":  # Wohnung kaufen
            base_url = "https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote"
        else:  # Wohnung mieten
            base_url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote"
        
        url = f"{base_url}?areaId={area_id}"
        
        if price_max:
            url += f"&PRICE_TO={price_max}"
        
        if area_min:
            url += f"&ESTATE_SIZE/LIVING_AREA_FROM={area_min}"
        
        logger.info(f"Direct URL: {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
    
    current_url = page.url
    logger.debug(f"Current URL: {current_url}")
    logger.success("Search results loaded")
    return page
