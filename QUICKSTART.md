# Quick Start Guide

## Install & Run

```bash
# Clone the repository
git clone https://github.com/JONTK123/SCRAPING-PROMILES.git
cd SCRAPING-PROMILES

# Quick start with script
./run.sh

# OR manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API URLs

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Quick Examples

### Using curl

```bash
# List airlines
curl http://localhost:8000/scrape/airlines

# Scrape LATAM with library method
curl -X POST http://localhost:8000/scrape/flight \
  -H "Content-Type: application/json" \
  -d '{"airline": "latam", "method": "library"}'

# Scrape GOL with regex method
curl -X POST http://localhost:8000/scrape/flight \
  -H "Content-Type: application/json" \
  -d '{"airline": "gol", "method": "regex"}'

# Scrape all airlines
curl http://localhost:8000/scrape/all?method=library
```

### Using Python

```python
import httpx
import asyncio

async def scrape_latam():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/scrape/flight",
            json={"airline": "latam", "method": "library"}
        )
        print(response.json())

asyncio.run(scrape_latam())
```

## Supported Airlines

| Airline | Code  | Program    | URL                                        |
|---------|-------|------------|--------------------------------------------|
| LATAM   | latam | LATAM Pass | https://www.latamairlines.com/br/pt        |
| GOL     | gol   | Smiles     | https://www.voegol.com.br/nh/              |
| AZUL    | azul  | TudoAzul   | https://www.voeazul.com.br/home/br/pt/home |

## Scraping Methods

1. **library** - Uses BeautifulSoup4 for HTML parsing (more robust)
2. **regex** - Uses regular expressions for pattern matching (faster)

## Response Format

```json
{
  "airline": "LATAM",
  "origin": "GRU",
  "destination": "RIO",
  "departure_date": "2024-12-01",
  "price_reais": 450.00,
  "price_miles": 15000,
  "scrape_method": "library",
  "scraped_at": "2024-10-27T11:16:51.986Z",
  "url": "https://www.latamairlines.com/br/pt",
  "status": "success",
  "error_message": null
}
```

## Testing

```bash
# Run extraction tests
python test_extraction.py

# Run example usage
python example_usage.py
```

## Project Structure

```
SCRAPING-PROMILES/
├── app/
│   ├── main.py           # FastAPI app
│   ├── models/           # Data models
│   ├── scrapers/         # Scraper implementations
│   └── routes/           # API endpoints
├── README.md             # Full documentation
├── CONTRIBUTING.md       # Developer guide
├── example_usage.py      # Usage examples
├── test_extraction.py    # Extraction tests
├── run.sh                # Quick start script
└── requirements.txt      # Dependencies
```

## Need Help?

- Check the full **README.md** for detailed documentation
- See **CONTRIBUTING.md** for development guidelines
- Visit **http://localhost:8000/docs** for interactive API documentation
