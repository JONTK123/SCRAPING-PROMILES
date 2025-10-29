from bs4 import BeautifulSoup
from typing import Dict, Optional
from .base_scraper import BaseScraper
from datetime import datetime


class LatamScraper(BaseScraper):
    """Scraper for LATAM Airlines"""
    
    def __init__(self):
        super().__init__(
            airline_name="LATAM",
            base_url="https://www.latamairlines.com/br/pt"
        )
    
    async def scrape_with_library(self, origin: Optional[str] = None, 
                                   destination: Optional[str] = None,
                                   departure_date: Optional[str] = None) -> Dict:
        """Scrape LATAM using BeautifulSoup library"""
        try:
            html = await self.fetch_page(self.base_url)
            soup = BeautifulSoup(html, 'lxml')
            
            # Try to find prices using common selectors
            price_reais = None
            price_miles = None
            
            # Look for price elements
            price_elements = soup.find_all(['span', 'div', 'p'], 
                                          class_=lambda x: x and any(word in str(x).lower() 
                                                                     for word in ['price', 'valor', 'preco']))
            
            for elem in price_elements:
                text = elem.get_text()
                if 'R$' in text or 'BRL' in text:
                    price_reais = self.extract_price_reais_regex(text)
                if 'milhas' in text.lower() or 'pontos' in text.lower():
                    price_miles = self.extract_price_miles_regex(text)
            
            # Search for LATAM Pass miles
            miles_elements = soup.find_all(text=lambda t: t and 'milhas' in t.lower())
            if miles_elements and not price_miles:
                for elem in miles_elements:
                    price_miles = self.extract_price_miles_regex(str(elem))
                    if price_miles:
                        break
            
            return {
                "airline": self.airline_name,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "price_reais": price_reais,
                "price_miles": price_miles,
                "scrape_method": "library",
                "scraped_at": datetime.now(),
                "url": self.base_url,
                "status": "success",
                "error_message": None
            }
        except Exception as e:
            return {
                "airline": self.airline_name,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "price_reais": None,
                "price_miles": None,
                "scrape_method": "library",
                "scraped_at": datetime.now(),
                "url": self.base_url,
                "status": "error",
                "error_message": str(e)
            }
    
    async def scrape_with_regex(self, origin: Optional[str] = None,
                                destination: Optional[str] = None,
                                departure_date: Optional[str] = None) -> Dict:
        """Scrape LATAM using regex patterns"""
        try:
            html = await self.fetch_page(self.base_url)
            
            # Extract prices using regex
            price_reais = self.extract_price_reais_regex(html)
            price_miles = self.extract_price_miles_regex(html)
            
            return {
                "airline": self.airline_name,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "price_reais": price_reais,
                "price_miles": price_miles,
                "scrape_method": "regex",
                "scraped_at": datetime.now(),
                "url": self.base_url,
                "status": "success",
                "error_message": None
            }
        except Exception as e:
            return {
                "airline": self.airline_name,
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "price_reais": None,
                "price_miles": None,
                "scrape_method": "regex",
                "scraped_at": datetime.now(),
                "url": self.base_url,
                "status": "error",
                "error_message": str(e)
            }
