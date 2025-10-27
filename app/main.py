from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import scrape

app = FastAPI(
    title="Airline Price Scraper API",
    description="API para scraping de preços de passagens aéreas (em reais e milhas) das companhias LATAM, GOL e AZUL",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scrape.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Airline Price Scraper API",
        "version": "1.0.0",
        "description": "API para scraping de preços de passagens aéreas",
        "endpoints": {
            "documentation": "/docs",
            "openapi_schema": "/openapi.json",
            "scrape_flight": "/scrape/flight",
            "scrape_all": "/scrape/all",
            "list_airlines": "/scrape/airlines"
        },
        "supported_airlines": ["LATAM", "GOL", "AZUL"],
        "scraping_methods": ["library (BeautifulSoup)", "regex (manual)"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
