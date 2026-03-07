# Willhaben.at Apartment Scraper

Automated web scraper for collecting real estate data from [willhaben.at](https://www.willhaben.at), Austria's largest classifieds platform. Built for market analysis and price monitoring of apartments in Graz (and other Austrian cities).

## Features

- **Automated Search** - Configure city, property type, price range, and size filters
- **Structured Data** - Extracts 30+ attributes per apartment (price, size, location, amenities, energy ratings)
- **Queue-Based Scraping** - Process search results page-by-page to avoid rate limiting
- **Anti-Detection** - Random delays, realistic browser fingerprints, stealth mode
- **GPS Coordinates** - Precise location data for mapping and analysis
- **JSON Export** - Clean, structured data ready for analysis
- **Cron-Ready** - Designed for periodic execution (hourly/daily)

## Extracted Data

Each apartment listing includes:

**Basic Info:**
- Title, description, district, full address
- Price (rent/purchase), extra costs
- Size (living area, useable area), number of rooms, floor

**Amenities:**
- Balcony, terrace, loggia, garden (with sizes)
- Garage, parking, elevator, basement
- Furnished status, pets allowed

**Building Details:**
- Building type, condition, year built
- Floor surface, heating type
- Energy ratings (HWB, FGEE classes)

**Location:**
- GPS coordinates (latitude, longitude)
- Availability date
- Listing type (private/agency)

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd webScraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configuration

Edit `config.py`:

```python
SEARCH_CONFIG = {
    "property_type": "101",  # 101 = Buy, 102 = Rent
    "city": "Graz",          # Graz, Wien, Linz, Salzburg, Innsbruck
    "price_max": 300000,     # Optional: max price
    "area_min": 50,          # Optional: min area in m²
}

HEADLESS = False  # Set True for background execution
```

### 3. Run Scraper

**Option A: One-time scraping (first 5 apartments)**
```bash
python main.py
```

**Option B: Queue-based scraping (recommended for large datasets)**
```bash
# Step 1: Collect all search result pages
python collect_pages.py

# Step 2: Scrape one page at a time
python scrape_page.py
```

## Project Structure

```
webScraper/
├── scraper/
│   ├── browser.py       # Browser automation with anti-detection
│   ├── parser.py        # HTML/JSON parsing and data extraction
│   ├── scraper.py       # Main scraping logic with rate limiting
│   └── __init__.py
├── data/
│   ├── apartments.json  # Scraped apartment data
│   └── pages_queue.json # Queue of pages to scrape
├── analysis/
│   └── analysis.ipynb   # Data analysis (coming soon)
├── collect_pages.py     # Collect search result page URLs
├── scrape_page.py       # Scrape one page from queue
├── main.py              # Simple one-time scraper
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
└── README.md
```

## Automated Workflow

The scraper is designed for periodic execution to continuously monitor the market.

### How It Works

1. **collect_pages.py** - Runs daily to refresh the search
   - Performs search on willhaben.at
   - Discovers all result pages (1, 2, 3... N)
   - Saves page URLs to `data/pages_queue.json`
   - Adds new pages without removing existing ones

2. **scrape_page.py** - Runs hourly to process one page
   - Takes first URL from queue
   - Scrapes all apartments from that page
   - Appends to `data/apartments.json` (deduplicates by URL)
   - Removes processed page from queue
   - Next run processes the next page

### Automation Setup

**Linux/Mac (crontab):**

```bash
# Edit crontab
crontab -e

# Add these lines:
# Collect pages daily at 6 AM
0 6 * * * cd /home/user/webScraper && venv/bin/python collect_pages.py >> logs/collect.log 2>&1

# Scrape one page every hour
0 * * * * cd /home/user/webScraper && venv/bin/python scrape_page.py >> logs/scrape.log 2>&1
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Hourly (or daily for collect_pages.py)
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `scrape_page.py`
   - Start in: `C:\path\to\webScraper`

### Monitoring

```bash
# Check queue status
python -c "import json; print(f'{len(json.load(open(\"data/pages_queue.json\")))} pages in queue')"

# Check scraped apartments
python -c "import json; print(f'{len(json.load(open(\"data/apartments.json\")))} apartments scraped')"
```

## Anti-Detection Features

- **Stealth Browser Settings** - Disables automation flags
- **Realistic User-Agent** - Chrome 120 on Windows
- **Austrian Locale** - de-AT locale, Vienna timezone
- **Random Delays** - 2-5 seconds between requests, 1-3 seconds after page load
- **Human-like Behavior** - Realistic viewport, network idle waits

## Advanced Usage

### Custom Search URL

If you need specific filters not in config:

```python
from scraper.browser import Browser

with Browser() as context:
    page = context.new_page()
    page.goto("https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?areaId=60101&PRICE_TO=300000")
    # ... scrape
```

### Scrape Specific URLs

Edit `config.py`:

```python
APARTMENT_URLS = [
    "https://www.willhaben.at/iad/immobilien/d/eigentumswohnung/...",
    "https://www.willhaben.at/iad/immobilien/d/eigentumswohnung/...",
]
```

Then run `main.py` - it will scrape these URLs instead of searching.

## Data Analysis

Data analysis is not included in this project. The scraped data (`data/apartments.json`) can be used in a separate analysis project for:
- Price vs. size correlation
- District comparison
- Amenity impact on pricing
- Market trends over time
- Interactive maps with GPS data

The JSON output is structured and ready for import into any data analysis tool (pandas, R, Excel, etc.).

## Legal & Ethical Considerations

- **Respect robots.txt** - Check willhaben.at's robots.txt
- **Rate Limiting** - Built-in delays to avoid overloading servers
- **Personal Use** - This tool is for personal research and analysis
- **No Redistribution** - Don't republish scraped data commercially
- **Terms of Service** - Review willhaben.at's ToS before use

## Troubleshooting

**"No search results found"**
- Check if willhaben.at changed their HTML structure
- Try setting `HEADLESS = False` to see what's happening

**"advertDetails not found"**
- The apartment listing might be expired or removed
- Parser will skip it and continue with next listing

**Browser crashes**
- Increase `TIMEOUT` in config.py
- Check available RAM (Chromium needs ~200MB per instance)

**Queue not processing**
- Verify `data/pages_queue.json` exists and is valid JSON
- Run `collect_pages.py` first to populate queue

## Contributing

Contributions welcome! Areas for improvement:
- Support for more Austrian cities
- Additional data fields
- Data visualization dashboards
- Database integration (PostgreSQL/MongoDB)
- Docker containerization

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Logging powered by [Loguru](https://github.com/Delgan/loguru)

---

**Note:** This scraper is for educational and personal use. Always respect website terms of service and rate limits.
