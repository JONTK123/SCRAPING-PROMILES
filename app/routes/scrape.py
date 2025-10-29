from fastapi import APIRouter, HTTPException
from typing import List
from app.models.flight import FlightPrice, ScrapeRequest
from app.scrapers.latam_scraper import LatamScraper
from app.scrapers.gol_scraper import GolScraper
from app.scrapers.azul_scraper import AzulScraper


router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/flight", response_model=FlightPrice)
async def scrape_flight_prices(request: ScrapeRequest):
    """
    Scrape flight prices from specified airline
    
    Parameters:
    - airline: "latam", "azul", or "gol"
    - method: "library" (BeautifulSoup) or "regex" (manual regex)
    - origin: Optional origin airport code
    - destination: Optional destination airport code
    - departure_date: Optional departure date
    
    Returns flight price information including prices in reais and miles
    """
    airline = request.airline.lower()
    method = request.method.lower()
    
    # Select scraper based on airline
    if airline == "latam":
        scraper = LatamScraper()
    elif airline == "gol":
        scraper = GolScraper()
    elif airline == "azul":
        scraper = AzulScraper()
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid airline. Must be one of: latam, gol, azul"
        )
    
    # Execute scraping based on method
    if method == "library":
        result = await scraper.scrape_with_library(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date
        )
    elif method == "regex":
        result = await scraper.scrape_with_regex(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid method. Must be 'library' or 'regex'"
        )
    
    return FlightPrice(**result)


@router.get("/all", response_model=List[FlightPrice])
async def scrape_all_airlines(method: str = "library"):
    """
    Scrape all airlines at once
    
    Parameters:
    - method: "library" (BeautifulSoup) or "regex" (manual regex)
    
    Returns list of flight price information from all airlines
    """
    method = method.lower()
    if method not in ["library", "regex"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid method. Must be 'library' or 'regex'"
        )
    
    scrapers = [
        LatamScraper(),
        GolScraper(),
        AzulScraper()
    ]
    
    results = []
    for scraper in scrapers:
        if method == "library":
            result = await scraper.scrape_with_library()
        else:
            result = await scraper.scrape_with_regex()
        results.append(FlightPrice(**result))
    
    return results


@router.get("/airlines")
async def list_airlines():
    """List supported airlines"""
    return {
        "airlines": [
            {
                "name": "LATAM",
                "code": "latam",
                "url": "https://www.latamairlines.com/br/pt",
                "program": "LATAM Pass"
            },
            {
                "name": "GOL",
                "code": "gol",
                "url": "https://www.voegol.com.br/nh/",
                "program": "Smiles"
            },
            {
                "name": "AZUL",
                "code": "azul",
                "url": "https://www.voeazul.com.br/home/br/pt/home",
                "program": "TudoAzul"
            }
        ]
    }
