import time
import random
import re
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # Required to locate elements
from selenium.webdriver.common.keys import Keys  # Required to press keys (like Enter)
from webdriver_manager.chrome import ChromeDriverManager



def scout_green_selenium():
    load_dotenv()
    print("Starting Selenium!")

    # 1. Browser Configuration (GUI mode)
    chrome_options = ChromeOptions()
    chrome_options.binary_location = os.getenv("BROWSER_LOCATION")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        # 2. Navigate to the main page
        url = "https://www.green-japan.com"
        print(f"🏃 Navigating to {url}...")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.url_contains(url))

        print("🔍 Locating the search bar...")

        # Use the input tag name="user_search[keyword]" identified earlier
        search_box = driver.find_element(By.NAME, "user_search[keyword]")

        print("✍️ Typing 'データエンジニア'...")
        search_box.clear()
        search_box.send_keys("データエンジニア")
        time.sleep(random.uniform(1, 3))  # Wait for 1 second (mimic human behavior)
        search_box.send_keys(Keys.RETURN)

        print("⏳ Waiting for results to load (5 seconds)...")
        # WebDriverWait(driver, 10).until(EC.url_contains("/search/result"))  # Wait for the page to load
        time.sleep(5)

        # 4. Verify Results
        print(f"📄 Current Page Title: {driver.title}")
        print(f"📍 Current URL: {driver.current_url}")

        if "search/result" in driver.current_url:
            print("✅ Successfully entered the search result page")
        else:
            print("🚨 Still on the wrong page? (Please check the screen manually!)")

        # 5. Data Extraction (Pass to BeautifulSoup)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        company_links = soup.find_all(
            "a", href=re.compile(r"^/company"), target="_blank"
        )
        real_job_cards = []
        seen_cards = set()

        for link in company_links:
            # Find parent container with 'MuiBox-root' class
            card = link.find_parent(class_=lambda x: x and "MuiBox-root" in x)
            if card and card not in seen_cards:
                real_job_cards.append(card)
                seen_cards.add(card)

        print(f"📦 Scanned cards count: {len(real_job_cards)}")

        match_count = 0
        jobs_list = []
        for i, card in enumerate(real_job_cards):

            def get_info(label):
                target_tag = card.find(attrs={"aria-label": label})
                if target_tag:
                    return target_tag.get_text(strip=True)
                return "-"

            occupation = get_info("募集職種")  # Job Type
            title_tag = card.find("h2", class_=lambda x: x and "job-offer-name" in x)
            title = title_tag.text.strip() if title_tag else "Untitled"

            # Filtering logic
            full_text = (occupation + title).lower()
            if "data" not in full_text and "データ" not in full_text:
                continue

            match_count += 1
            print(f"\n🎉 Found #{match_count}")

            company = "-"
            try:
                company = card.select(".MuiTypography-subtitle2")[0].text.strip()
            except:
                company = "-"

            print(f"🏢 Company: {company}")
            print(f"📜 Title: {title}")
            print(f"🔧 Occupation: {occupation}")
            print(f"💰 Salary: {get_info('想定年収')}")
            print(f"📍 Location: {get_info('勤務地')}")
            print(f"⌨️ Tech stack: {get_info('関連スキル')}")
            print(f"🔗 Link: https://www.green-japan.com{link['href']}")

            job_info = {
                "Company": company,
                "Title": title,
                "Occupation": occupation,
                "Salary": get_info("想定年収"),
                "Location": get_info("勤務地"),
                "Tech stack": get_info("関連スキル"),
                "Link": f"https://www.green-japan.com{link['href']}",
            }
            jobs_list.append(job_info)
            if match_count >= 5:
                break

        # save results to a JSON after the loop
        if jobs_list:
            today=datetime.now().strftime("%Y_%m_%d")
            raw_data_env = os.getenv("RAW_DATA_DIR", "./data/raw_data")
            
            if raw_data_env:
                raw_data_dir = Path(raw_data_env)
            else:
                raw_data_dir = Path(__file__).parent.parent.parent / "data" / "raw_data"

            raw_data_dir.mkdir(parents=True, exist_ok=True)
            output_path = raw_data_dir / f"scout_green_jobs_{today}.json"
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(jobs_list, f, ensure_ascii=False, indent=4)

        if match_count == 0:
            print("\n💨 No matches found. (Please check the browser screen!)")

    except Exception as e:
        print(f"❌ Error occurred: {e}")

    finally:
        print("\n👋 Closing browser in 30 seconds... (Check the results!)")
        time.sleep(30)  # Extended time for manual inspection
        driver.quit()  # Close the browser regardless of success or failure


if __name__ == "__main__":
    scout_green_selenium()
