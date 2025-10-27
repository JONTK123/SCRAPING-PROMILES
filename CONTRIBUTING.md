# Contributing to Airline Price Scraper

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/JONTK123/SCRAPING-PROMILES.git
cd SCRAPING-PROMILES
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided script:
```bash
./run.sh
```

## Project Structure

```
SCRAPING-PROMILES/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   └── flight.py        # Pydantic models for data validation
│   ├── scrapers/
│   │   ├── base_scraper.py  # Abstract base class for all scrapers
│   │   ├── latam_scraper.py # LATAM airline scraper
│   │   ├── gol_scraper.py   # GOL airline scraper
│   │   └── azul_scraper.py  # AZUL airline scraper
│   └── routes/
│       └── scrape.py        # API route definitions
├── example_usage.py         # Example API usage
├── test_extraction.py       # Extraction method tests
└── requirements.txt         # Python dependencies
```

## Adding a New Airline Scraper

To add a new airline scraper:

1. Create a new file in `app/scrapers/` (e.g., `new_airline_scraper.py`)

2. Inherit from `BaseScraper` and implement required methods:

```python
from bs4 import BeautifulSoup
from typing import Dict, Optional
from .base_scraper import BaseScraper
from datetime import datetime


class NewAirlineScraper(BaseScraper):
    """Scraper for New Airline"""
    
    def __init__(self):
        super().__init__(
            airline_name="NEW_AIRLINE",
            base_url="https://www.newairline.com"
        )
    
    async def scrape_with_library(self, origin: Optional[str] = None,
                                   destination: Optional[str] = None,
                                   departure_date: Optional[str] = None) -> Dict:
        """Implement library-based scraping with BeautifulSoup"""
        try:
            html = await self.fetch_page(self.base_url)
            soup = BeautifulSoup(html, 'lxml')
            
            # Your scraping logic here
            price_reais = None
            price_miles = None
            
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
        """Implement regex-based scraping"""
        try:
            html = await self.fetch_page(self.base_url)
            
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
```

3. Update `app/routes/scrape.py` to include the new scraper:

```python
from app.scrapers.new_airline_scraper import NewAirlineScraper

# Add to the scrape_flight_prices function
if airline == "newairline":
    scraper = NewAirlineScraper()
```

4. Update the `/scrape/airlines` endpoint to list the new airline

## Testing

Run the extraction tests:
```bash
python test_extraction.py
```

Run the example usage:
```bash
# Make sure the server is running first
python example_usage.py
```

## API Documentation

After starting the server, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Important Notes

- Always respect the terms of service of websites being scraped
- Be mindful of rate limiting and add delays if necessary
- Handle errors gracefully
- Test your changes thoroughly before submitting

## Questions?

Feel free to open an issue on GitHub if you have any questions or need help!
