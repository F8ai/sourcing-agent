"""
Web Scraper for Cannabis Industry Sources
Collects data from supplier websites for the sourcing agent
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import json
import time
import logging
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CannabisSourceScraper:
    """Scraper for cannabis industry supplier websites"""
    
    def __init__(self, sources_file: str = "sources/sources.json"):
        self.sources_file = sources_file
        self.sources_data = self._load_sources()
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _load_sources(self) -> Dict[str, Any]:
        """Load sources data from JSON file"""
        try:
            with open(self.sources_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading sources file: {e}")
            return {}
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
        return self.session
    
    async def close_session(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def scrape_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape a single source website"""
        url = source.get('url')
        if not url:
            return {'error': 'No URL provided'}
        
        try:
            session = await self._get_session()
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            logger.info(f"Scraping: {url}")
            
            async with session.get(url, allow_redirects=True) as response:
                if response.status != 200:
                    return {
                        'url': url,
                        'error': f'HTTP {response.status}',
                        'status': response.status
                    }
                
                content = await response.text()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract data
                scraped_data = {
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success',
                    'title': self._extract_title(soup),
                    'description': self._extract_description(soup),
                    'products': self._extract_products(soup, source),
                    'contact_info': self._extract_contact_info(soup),
                    'location': self._extract_location(soup, source),
                    'certifications': self._extract_certifications(soup),
                    'services': self._extract_services(soup, source)
                }
                
                return scraped_data
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Try h1 tags
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description"""
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Try Open Graph description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        # Try first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text().strip()
            if len(text) > 50:  # Only if it's substantial
                return text[:200] + "..." if len(text) > 200 else text
        
        return ""
    
    def _extract_products(self, soup: BeautifulSoup, source: Dict[str, Any]) -> List[str]:
        """Extract product information"""
        products = []
        
        # Look for product-related keywords
        product_keywords = [
            'product', 'products', 'catalog', 'shop', 'store', 'buy',
            'seeds', 'clones', 'nutrients', 'equipment', 'lighting',
            'packaging', 'containers', 'supplies', 'accessories'
        ]
        
        # Check navigation and menu items
        nav_items = soup.find_all(['a', 'li'], class_=re.compile(r'nav|menu|product'))
        for item in nav_items:
            text = item.get_text().strip().lower()
            if any(keyword in text for keyword in product_keywords):
                products.append(item.get_text().strip())
        
        # Check for product lists
        product_elements = soup.find_all(['div', 'section'], class_=re.compile(r'product|item|card'))
        for element in product_elements[:10]:  # Limit to first 10
            title = element.find(['h2', 'h3', 'h4'])
            if title:
                products.append(title.get_text().strip())
        
        # Add known products from source data
        if source.get('products'):
            products.extend(source['products'])
        
        return list(set(products))  # Remove duplicates
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}
        
        # Look for contact information patterns
        contact_patterns = {
            'phone': r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'address': r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct))'
        }
        
        page_text = soup.get_text()
        
        for info_type, pattern in contact_patterns.items():
            matches = re.findall(pattern, page_text)
            if matches:
                contact_info[info_type] = matches[0]
        
        # Look for contact links
        contact_links = soup.find_all('a', href=re.compile(r'mailto:|tel:'))
        for link in contact_links:
            href = link.get('href', '')
            if href.startswith('mailto:'):
                contact_info['email'] = href.replace('mailto:', '')
            elif href.startswith('tel:'):
                contact_info['phone'] = href.replace('tel:', '')
        
        return contact_info
    
    def _extract_location(self, soup: BeautifulSoup, source: Dict[str, Any]) -> str:
        """Extract location information"""
        # First try to get from source data
        if source.get('location'):
            return source['location']
        
        # Look for address information in the page
        address_patterns = [
            r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)[^,]*,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5})',
            r'([A-Za-z\s]+,\s*[A-Z]{2})',
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+)'
        ]
        
        page_text = soup.get_text()
        
        for pattern in address_patterns:
            matches = re.findall(pattern, page_text)
            if matches:
                return matches[0].strip()
        
        return ""
    
    def _extract_certifications(self, soup: BeautifulSoup) -> List[str]:
        """Extract certification information"""
        certifications = []
        
        # Look for certification keywords
        cert_keywords = [
            'certified', 'certification', 'licensed', 'license', 'approved',
            'omri', 'organic', 'usda', 'fda', 'iso', 'gmp', 'haccp',
            'kosher', 'halal', 'vegan', 'gluten-free'
        ]
        
        page_text = soup.get_text().lower()
        
        for keyword in cert_keywords:
            if keyword in page_text:
                # Find the context around the keyword
                index = page_text.find(keyword)
                start = max(0, index - 50)
                end = min(len(page_text), index + 50)
                context = page_text[start:end]
                certifications.append(context.strip())
        
        return list(set(certifications))
    
    def _extract_services(self, soup: BeautifulSoup, source: Dict[str, Any]) -> List[str]:
        """Extract services information"""
        services = []
        
        # Add known services from source data
        if source.get('services'):
            services.extend(source['services'])
        
        # Look for service-related keywords
        service_keywords = [
            'service', 'services', 'consulting', 'training', 'support',
            'installation', 'maintenance', 'repair', 'warranty',
            'custom', 'design', 'engineering', 'compliance'
        ]
        
        # Check for service sections
        service_elements = soup.find_all(['div', 'section'], class_=re.compile(r'service|consulting|support'))
        for element in service_elements:
            title = element.find(['h2', 'h3', 'h4'])
            if title:
                services.append(title.get_text().strip())
        
        return list(set(services))
    
    async def scrape_all_sources(self, max_concurrent: int = 5) -> Dict[str, Any]:
        """Scrape all sources with rate limiting"""
        all_sources = []
        
        # Collect all sources
        if self.sources_data.get('preferred_sources'):
            all_sources.extend(self.sources_data['preferred_sources'])
        
        if self.sources_data.get('sources_by_state'):
            for state, state_data in self.sources_data['sources_by_state'].items():
                if state_data.get('materials'):
                    all_sources.extend(state_data['materials'])
                if state_data.get('equipment'):
                    all_sources.extend(state_data['equipment'])
        
        if self.sources_data.get('national_suppliers'):
            if self.sources_data['national_suppliers'].get('materials'):
                all_sources.extend(self.sources_data['national_suppliers']['materials'])
            if self.sources_data['national_suppliers'].get('equipment'):
                all_sources.extend(self.sources_data['national_suppliers']['equipment'])
        
        logger.info(f"Found {len(all_sources)} sources to scrape")
        
        # Scrape with rate limiting
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_semaphore(source):
            async with semaphore:
                result = await self.scrape_source(source)
                # Add delay to be respectful
                await asyncio.sleep(1)
                return result
        
        tasks = [scrape_with_semaphore(source) for source in all_sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_scrapes = []
        failed_scrapes = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_scrapes.append({
                    'source': all_sources[i],
                    'error': str(result)
                })
            elif result.get('status') == 'success':
                successful_scrapes.append(result)
            else:
                failed_scrapes.append(result)
        
        return {
            'total_sources': len(all_sources),
            'successful_scrapes': len(successful_scrapes),
            'failed_scrapes': len(failed_scrapes),
            'results': successful_scrapes,
            'failures': failed_scrapes,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_scraped_data(self, data: Dict[str, Any], filename: str = None):
        """Save scraped data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sources/scraped_data_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Scraped data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving scraped data: {e}")

async def main():
    """Main function for testing the scraper"""
    scraper = CannabisSourceScraper()
    
    try:
        print("Starting cannabis source scraping...")
        results = await scraper.scrape_all_sources(max_concurrent=3)
        
        print(f"Scraping completed:")
        print(f"  Total sources: {results['total_sources']}")
        print(f"  Successful: {results['successful_scrapes']}")
        print(f"  Failed: {results['failed_scrapes']}")
        
        # Save results
        scraper.save_scraped_data(results)
        
    finally:
        await scraper.close_session()

if __name__ == "__main__":
    asyncio.run(main()) 