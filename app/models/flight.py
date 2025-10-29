from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlightPrice(BaseModel):
    """Model for flight price information"""
    airline: str
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    price_reais: Optional[float] = None
    price_miles: Optional[int] = None
    scrape_method: str  # "library" or "regex"
    scraped_at: datetime = datetime.now()
    url: str
    status: str  # "success" or "error"
    error_message: Optional[str] = None


class ScrapeRequest(BaseModel):
    """Model for scrape request"""
    airline: str  # "latam", "azul", or "gol"
    method: str = "library"  # "library" or "regex"
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
