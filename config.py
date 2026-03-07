# Browser settings
HEADLESS = False  # Set to False to see browser (helps avoid detection)
TIMEOUT = 30000  # milliseconds

# Search settings
SEARCH_CONFIG = {
    # Property type: 101 = Wohnung kaufen, 102 = Wohnung mieten
    "property_type": "101",
    
    # Location
    "city": "Graz",
    
    # Price range (optional)
    "price_max": None,  # e.g. 300000
    
    # Living area (optional)
    "area_min": None,  # e.g. 50 (m²)
    
    # Number of rooms (optional)
    "rooms_min": None,  # e.g. 2
    
    # Max pages to scrape (None = all pages)
    "max_pages": None,
}
