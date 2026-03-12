from bs4 import BeautifulSoup
from loguru import logger
import json
import re
import html as html_module


def clean_html(text):
    """Ukloni HTML tagove i očisti tekst"""
    if not text:
        return None
    text = html_module.unescape(text)
    soup = BeautifulSoup(text, 'lxml')
    clean = soup.get_text(separator=' ', strip=True)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip() if clean else None


def parse_list_items(html_text):
    """Parsira <ul><li> liste u dictionary"""
    if not html_text or '<li>' not in html_text:
        return None
    
    soup = BeautifulSoup(html_text, 'lxml')
    items = {}
    
    for li in soup.find_all('li'):
        text = li.get_text(strip=True)
        if ':' in text:
            key, value = text.split(':', 1)
            items[key.strip()] = value.strip()
        else:
            items[text] = True
    
    return items if items else clean_html(html_text)


def parse_structured_text(html_text):
    """Parsira strukturirani tekst sa <strong> naslovima"""
    if not html_text or '<strong>' not in html_text:
        return clean_html(html_text)
    
    soup = BeautifulSoup(html_text, 'lxml')
    sections = {}
    current_section = None
    
    for element in soup.descendants:
        if element.name == 'strong':
            current_section = element.get_text(strip=True).rstrip(':')
            sections[current_section] = []
        elif element.name == 'br' and current_section:
            continue
        elif isinstance(element, str) and current_section:
            text = element.strip()
            if text and text not in sections[current_section]:
                sections[current_section].append(text)
    
    return {k: ' '.join(v) for k, v in sections.items() if v} or clean_html(html_text)


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
    Dinamički parsira apartman podatke iz willhaben.at HTML-a.
    Koristi originalne njemačke ključeve bez hardkodiranja.
    """
    soup = BeautifulSoup(html, 'lxml')
    
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if not script_tag:
        logger.error(f"No __NEXT_DATA__ found for {url}")
        return None
    
    try:
        data = json.loads(script_tag.string)
        page_props = data['props']['pageProps']
        
        if 'advertDetails' not in page_props:
            logger.error(f"No advertDetails in pageProps for {url}")
            return None
        
        ad = page_props['advertDetails']
        apartment = {'url': url}
        
        # Osnovni podaci
        for key in ['id', 'uuid', 'description', 'advertiserReferenceNumber', 
                    'createdDate', 'changedDate', 'publishedDate']:
            if key in ad:
                apartment[key] = ad[key]
        
        # Adresa
        address_details = ad.get('advertAddressDetails', {})
        if address_details:
            apartment['advertAddressDetails'] = {
                'postalCode': address_details.get('postalCode'),
                'postalName': address_details.get('postalName'),
                'addressLines': address_details.get('addressLines', {}).get('value', [])
            }
        
        # Dinamički parsiraj SVE atribute
        for attr in ad.get('attributes', {}).get('attribute', []):
            name = attr['name']
            values = attr.get('values', [])
            value = values[0] if len(values) == 1 else values
            
            # GENERAL_TEXT_ADVERT/ sekcije - koristi originalne njemačke nazive
            if name.startswith('GENERAL_TEXT_ADVERT/'):
                section_name = name.replace('GENERAL_TEXT_ADVERT/', '')
                
                if '<li>' in str(value):
                    parsed = parse_list_items(value)
                elif '<strong>' in str(value):
                    parsed = parse_structured_text(value)
                else:
                    parsed = clean_html(value)
                
                apartment[section_name] = parsed
            else:
                # Svi ostali atributi - direktno sa originalnim nazivom
                apartment[name] = value
        
        # Izvuci sekcije iz HTML-a (Objektinformationen, Ausstattung und Freiflächen)
        skip_sections = ['Premium Services', 'Verfügbare Wohneinheiten', 'Über dieses Neubauprojekt']
        
        for h2 in soup.find_all('h2'):
            section_title = h2.get_text(strip=True)
            
            if not section_title or len(section_title) > 100 or section_title in skip_sections:
                continue
            
            # Nađi sljedeći div sa atributima
            next_div = h2.find_next('div', {'data-testid': 'attribute-group'})
            if next_div:
                section_data = {}
                
                for item in next_div.find_all('li', {'data-testid': 'attribute-item'}):
                    title_div = item.find('div', {'data-testid': 'attribute-title'})
                    value_div = item.find('div', {'data-testid': 'attribute-value'})
                    
                    if title_div and value_div:
                        key = title_div.get_text(strip=True)
                        value = value_div.get_text(strip=True)
                        
                        if value_div.find('svg'):
                            section_data[key] = True
                        else:
                            section_data[key] = value
                
                if section_data:
                    apartment[section_title] = section_data
        
        # Izvuci Objektbeschreibung iz HTML-a
        for h2 in soup.find_all('h2'):
            if 'Objektbeschreibung' in h2.get_text():
                desc_div = h2.find_next('div', {'data-testid': lambda x: x and 'ad-description' in x})
                if desc_div:
                    apartment['Objektbeschreibung'] = clean_html(str(desc_div))
        
        logger.success(f"Parsed: {apartment.get('description', 'Unknown')[:50]}...")
        return apartment
        
    except Exception as e:
        logger.error(f"Error parsing {url}: {e}")
        return None
