from bs4 import BeautifulSoup
from loguru import logger
import json


def extract_search_results(html, max_results=None):
    """
    Extract apartment URLs from search results page
    
    Args:
        html: HTML content of search results page
        max_results: Maximum number of results to extract (None = all)
    
    Returns:
        List of apartment URLs
    """
    soup = BeautifulSoup(html, 'lxml')
    script = soup.find('script', {'id': '__NEXT_DATA__'})
    
    if not script:
        logger.error("__NEXT_DATA__ not found in search results")
        return []
    
    data = json.loads(script.string)
    
    # Try both possible paths (depends on how page was loaded)
    page_props = data['props']['pageProps']
    if 'searchResult' in page_props:
        search_result = page_props['searchResult']
    elif 'initialSearchResult' in page_props:
        search_result = page_props['initialSearchResult']
    else:
        logger.error("No search results found in pageProps")
        return []
    
    ads = search_result['advertSummaryList'].get('advertSummary', [])
    
    total = search_result.get('rowsFound', 0)
    logger.info(f"Found {total} total apartments in search results")
    
    urls = []
    for ad in ads[:max_results] if max_results else ads:
        ad_id = ad.get('id')
        
        # Extract correct URL from contextLinkList
        context_links = ad.get('contextLinkList', {}).get('contextLink', [])
        url = None
        
        for link in context_links:
            uri = link.get('uri', '')
            # Find the link with /d/ pattern and matching ID
            if '/d/' in uri and str(ad_id) in uri and 'api.willhaben.at' in uri:
                # Convert API URL to web URL
                url = uri.replace('https://api.willhaben.at/restapi/v2/atverz/', 'https://www.willhaben.at/iad/')
                break
        
        if url:
            urls.append(url)
        else:
            logger.warning(f"Could not find URL for ad {ad_id}")
    
    logger.success(f"Extracted {len(urls)} apartment URLs")
    return urls


def parse_apartment(html, url):
    """
    Parse apartment data from willhaben.at HTML.
    Data is stored in Next.js __NEXT_DATA__ script tag.
    """
    soup = BeautifulSoup(html, 'lxml')
    
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if not script_tag:
        logger.error(f"No __NEXT_DATA__ found for {url}")
        return None
    
    try:
        data = json.loads(script_tag.string)
        page_props = data['props']['pageProps']
        
        # Check if advertDetails exists
        if 'advertDetails' not in page_props:
            logger.error(f"No advertDetails in pageProps for {url}")
            logger.debug(f"Available keys: {list(page_props.keys())}")
            return None
        
        ad = page_props['advertDetails']
        attrs = {attr['name']: attr.get('values', []) for attr in ad.get('attributes', {}).get('attribute', [])}
        
        def get_attr(name, index=0):
            values = attrs.get(name, [])
            return values[index] if values and len(values) > index else None
        
        def attr_contains(name, keyword):
            values = attrs.get(name, [])
            return any(keyword.lower() in str(v).lower() for v in values)
        
        coords = get_attr('COORDINATES')
        lat, lon = (coords.split(',') if coords else [None, None])
        
        address_lines = ad.get('advertAddressDetails', {}).get('addressLines', {}).get('value', [])
        
        apartment_data = {
            "url": url,
            "title": ad.get('description', ''),
            "district": ad.get('advertAddressDetails', {}).get('postalName', ''),
            "address": ', '.join(address_lines) if address_lines else '',
            "price_rent": int(get_attr('PRICE') or 0),
            "extra_costs": get_attr('ADDITIONAL_COST/FEE'),
            "total_price": int(get_attr('PRICE') or 0),
            "size_m2": int(float((get_attr('ESTATE_SIZE/LIVING_AREA') or get_attr('ESTATE_SIZE') or '0').replace(',', '.'))),
            "useable_area": float(get_attr('ESTATE_SIZE/USEABLE_AREA').replace(',', '.')) if get_attr('ESTATE_SIZE/USEABLE_AREA') else None,
            "rooms": int(get_attr('NO_OF_ROOMS') or 0),
            "floor": get_attr('FLOOR'),
            "year_built": get_attr('CONSTRUCTION_YEAR'),
            "balcony": attr_contains('FREE_AREA/FREE_AREA_TYPE', 'balkon'),
            "terrace": attr_contains('FREE_AREA/FREE_AREA_TYPE', 'terrasse'),
            "garage": attr_contains('ESTATE_PREFERENCE', 'garage'),
            "parking": attr_contains('ESTATE_PREFERENCE', 'parkplatz') or attr_contains('ESTATE_PREFERENCE', 'stellplatz'),
            "elevator": attr_contains('ESTATE_PREFERENCE', 'fahrstuhl') or attr_contains('ESTATE_PREFERENCE', 'lift'),
            "furnished": attr_contains('ESTATE_PREFERENCE', 'möbliert'),
            "pets_allowed": attr_contains('ESTATE_PREFERENCE', 'haustier'),
            "keller": attr_contains('ESTATE_PREFERENCE', 'keller'),
            "garden": attr_contains('FREE_AREA/FREE_AREA_TYPE', 'garten'),
            "loggia": attr_contains('FREE_AREA/FREE_AREA_TYPE', 'loggia'),
            "latitude": float(lat) if lat else None,
            "longitude": float(lon) if lon else None,
            "description": get_attr('DESCRIPTION', 0) or '',
            "scraped_at": ad.get('changedDate', ''),
            "building_type": get_attr('BUILDING_TYPE'),
            "building_condition": get_attr('BUILDING_CONDITION'),
            "floor_surface": get_attr('FLOOR_SURFACE'),
            "heating": attrs.get('HEATING', []),
            "energy_hwb": get_attr('ENERGY_HWB'),
            "energy_hwb_class": get_attr('ENERGY_HWB_CLASS'),
            "energy_fgee": get_attr('ENERGY_FGEE'),
            "energy_fgee_class": get_attr('ENERGY_FGEE_CLASS'),
            "balcony_size": get_attr('FREE_AREA/FREE_AREA_AREA'),
            "available": get_attr('AVAILABLE_NOW'),
            "is_private": get_attr('ISPRIVATE') == '1',
        }
        
        logger.success(f"Parsed: {apartment_data['title'][:50]}...")
        return apartment_data
        
    except Exception as e:
        logger.error(f"Error parsing {url}: {e}")
        return None
