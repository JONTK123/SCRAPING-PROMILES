from abc import ABC, abstractmethod
from typing import Dict, Optional
import httpx
import re
from datetime import datetime


class BaseScraper(ABC):
    """Base scraper class with common functionality"""
    
    def __init__(self, airline_name: str, base_url: str):
        self.airline_name = airline_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    async def fetch_page(self, url: str) -> str:
        """Fetch page content"""
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
    
    @abstractmethod
    async def scrape_with_library(self, **kwargs) -> Dict:
        """Scrape using BeautifulSoup library"""
        pass
    
    @abstractmethod
    async def scrape_with_regex(self, **kwargs) -> Dict:
        """Scrape using regex patterns"""
        pass
    
    def extract_price_reais_regex(self, html: str) -> Optional[float]:
        """Extract price in reais using regex"""
        patterns = [
            r'R\$\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'BRL\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'reais[:\s]*(\d+(?:\.\d{3})*(?:,\d{2})?)',
            r'(?:price|valor|preço)["\s:]*R\$?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                price_str = match.group(1).replace('.', '').replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        return None
    
    def extract_price_miles_regex(self, html: str) -> Optional[int]:
        """Extract price in miles using regex"""
        patterns = [
            r'(\d+(?:\.\d{3})*)\s*(?:milhas|miles|pontos)',
            r'(?:milhas|miles|pontos)[:\s]*(\d+(?:\.\d{3})*)',
            r'(?:LATAM Pass|Smiles|TudoAzul)[:\s]*(\d+(?:\.\d{3})*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                miles_str = match.group(1).replace('.', '')
                try:
                    return int(miles_str)
                except ValueError:
                    continue
        return None
