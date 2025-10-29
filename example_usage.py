"""
Example usage of the Airline Price Scraper API

This script demonstrates how to use the API endpoints.
In a real environment with internet access, the scrapers would fetch
actual data from the airline websites.
"""

import httpx
import asyncio
import json


async def main():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("AIRLINE PRICE SCRAPER - EXAMPLE USAGE")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Check API health
        print("\n1. Checking API health...")
        response = await client.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # 2. List supported airlines
        print("\n2. Listing supported airlines...")
        response = await client.get(f"{base_url}/scrape/airlines")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 3. Scrape LATAM with library method
        print("\n3. Scraping LATAM with BeautifulSoup (library method)...")
        response = await client.post(
            f"{base_url}/scrape/flight",
            json={
                "airline": "latam",
                "method": "library",
                "origin": "GRU",
                "destination": "RIO",
                "departure_date": "2024-12-01"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 4. Scrape GOL with regex method
        print("\n4. Scraping GOL with Regex method...")
        response = await client.post(
            f"{base_url}/scrape/flight",
            json={
                "airline": "gol",
                "method": "regex",
                "origin": "SAO",
                "destination": "BSB"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 5. Scrape AZUL with library method
        print("\n5. Scraping AZUL with BeautifulSoup (library method)...")
        response = await client.post(
            f"{base_url}/scrape/flight",
            json={
                "airline": "azul",
                "method": "library"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        print("\n" + "=" * 60)
        print("NOTE: In a sandboxed environment without internet access,")
        print("the scrapers will return errors. In production with internet")
        print("access, they will fetch real data from airline websites.")
        print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the API server is running:")
    print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\nStarting examples...\n")
    asyncio.run(main())
