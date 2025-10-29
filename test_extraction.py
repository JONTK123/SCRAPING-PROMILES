"""
Unit tests to demonstrate the scrapers' extraction capabilities
with mock HTML data
"""

import asyncio
import re
from app.scrapers.base_scraper import BaseScraper


class MockScraper(BaseScraper):
    """Mock scraper for testing purposes"""
    
    def __init__(self):
        super().__init__("MOCK", "http://mock.com")
    
    async def scrape_with_library(self, **kwargs):
        return {}
    
    async def scrape_with_regex(self, **kwargs):
        return {}


def test_regex_price_extraction():
    """Test regex extraction methods"""
    scraper = MockScraper()
    
    print("=" * 60)
    print("TESTING REGEX EXTRACTION METHODS")
    print("=" * 60)
    
    # Test 1: Extract price in reais
    print("\n1. Testing extraction of prices in REAIS (R$):")
    mock_html_reais = """
    <div class="price">
        <span>Preço: R$ 1.234,56</span>
    </div>
    <div>Valor total: R$ 850,00</div>
    <p>A partir de BRL 2345.67</p>
    """
    price_reais = scraper.extract_price_reais_regex(mock_html_reais)
    print(f"   Mock HTML contains: R$ 1.234,56, R$ 850,00, BRL 2345.67")
    print(f"   Extracted price: R$ {price_reais}")
    
    # Test 2: Extract price in miles
    print("\n2. Testing extraction of prices in MILHAS/PONTOS:")
    mock_html_miles = """
    <div class="miles">
        <span>15.000 milhas</span>
    </div>
    <div>LATAM Pass: 25000 pontos</div>
    <p>A partir de 18.500 miles</p>
    """
    price_miles = scraper.extract_price_miles_regex(mock_html_miles)
    print(f"   Mock HTML contains: 15.000 milhas, 25000 pontos, 18.500 miles")
    print(f"   Extracted miles: {price_miles}")
    
    # Test 3: Multiple formats
    print("\n3. Testing various price formats:")
    test_cases = [
        ("R$ 450,00", scraper.extract_price_reais_regex),
        ("R$ 1.200,50", scraper.extract_price_reais_regex),
        ("BRL 999.99", scraper.extract_price_reais_regex),
        ("35000 milhas", scraper.extract_price_miles_regex),
        ("12.500 pontos", scraper.extract_price_miles_regex),
        ("TudoAzul: 20000", scraper.extract_price_miles_regex),
    ]
    
    for text, extractor in test_cases:
        result = extractor(text)
        print(f"   '{text}' -> {result}")
    
    print("\n" + "=" * 60)
    print("EXTRACTION METHODS DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nNOTE: These are the regex patterns used by the scraper")
    print("to extract prices from airline websites. In production,")
    print("the library method uses BeautifulSoup to parse HTML first,")
    print("then applies these patterns to extract the values.")
    print("=" * 60)


if __name__ == "__main__":
    test_regex_price_extraction()
