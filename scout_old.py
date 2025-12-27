"""
[Archive] Request-based Scraper Implementation
Filename: scout_old.py

Description:
  This script attempts to scrape 'Green Japan' using the `requests` library with Session and Headers handling.
  
  Note:
  - Green Japan uses Client-Side Rendering (CSR) with heavy JavaScript and strict bot detection.
  - While this script successfully manages Cookies and Headers (Referer), it gets redirected to the main page or fails to load dynamic content.
  - The working solution uses Selenium to handle JS rendering (not included in this file).

  This code is preserved for study purposes and as a reference for scraping static websites.
"""

import requests
import re
from bs4 import BeautifulSoup
import time

def scout_green_requests():
    # 1. Start Session
    session = requests.Session()

    # 2. Configure Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
        "Referer": "https://www.green-japan.com/",
    }
    session.headers.update(headers)

    print("🚪 [Old] Visiting main page to acquire cookies...")
    try:
        session.get("https://www.green-japan.com")
        time.sleep(1)

        print("🏃 [Old] Attempting search with cookies...")
        target_url = "https://www.green-japan.com/search/result"
        params = {"keyword": "データエンジニア"}
        
        response = session.get(target_url, params=params)
        print(f"📍 Final URL: {response.url}")

        if "search/result" in response.url:
            print("✅ Success! (But likely blocked by CSR)")
        else:
            print("🚨 Redirected to main page (Blocked)")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scout_green_requests()