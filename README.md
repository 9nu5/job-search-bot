# 🕵️‍♂️ Green Japan Job Scraper (Data Engineer Edition)

A Python-based web scraper designed to extract "Data Engineer" job listings from Green Japan, one of the leading IT/Web recruitment platforms in Japan.

This project overcomes strict anti-bot measures and Client-Side Rendering (CSR) issues using **Selenium** to filter out advertisements and irrelevant listings, ensuring high-quality search results.



## 🛠 Technologies Used

* **Python 3.x**
* **Selenium**: For browser automation and handling dynamic JavaScript content.
* **BeautifulSoup4**: For parsing HTML and extracting specific data points.
* **Requests**: Used in the initial research phase (archived in `scout_old.py`).
* **WebDriver Manager**: For automatic management of Chrome drivers.



## ✨ Features

* **Human-like Browsing**: Uses Selenium to mimic real user behavior (typing, clicking) to bypass redirects and bot detection.
* **Targeted Keyword Search**: specifically searches for "Data Engineer" (データエンジニア).
* **Smart Filtering**:
    * Removes Advertisements that appear at the top of search results.
    * Strictly filters out irrelevant roles (e.g., Sales, General Web Engineers) unless they explicitly mention "Data" or "データ".
* **Data Extraction**: Scrapes key details including:
    * Company Name
    * Job Title
    * Occupation Type
    * Salary Range
    * Location
    * Tech Stack / Skills (extracted via `aria-label`)



## 🔄 Process

1.  **Initial Analysis (X-Ray)**: Analyzed the HTML structure of Green Japan and identified that key information (like skills) was hidden in `aria-label` attributes.
2.  **Challenge (CSR & Bot Detection)**:
    * Initially attempted using `requests` with Headers and Session cookies.
    * Discovered that Green Japan redirects direct URL access to the main page and relies heavily on JavaScript for rendering results.
3.  **Solution (Selenium)**:
    * Switched to **Selenium** to launch a real Chrome browser instance.
    * Implemented a sequence: `Home Page` -> `Type Keyword` -> `Press Enter` to successfully land on the result page.
4.  **Refinement (Filtering)**:
    * Implemented a Python-based filter to exclude unrelated listings (Sales, Web Devs) that appeared due to the platform's recommendation algorithm.



## 📚 What I Learned

* **CSR vs SSR**: Understood the limitations of `requests` when dealing with Client-Side Rendering (CSR) websites.
* **Anti-Bot Mechanisms**: Learned about `Referer` headers, Cookies, and how websites detect bots by checking for JavaScript execution.
* **DOM Manipulation**: Gained experience in selecting elements using `aria-label` and dealing with dynamic class names.
* **Troubleshooting**: The importance of keeping failed attempts (`scout_old.py`) as a reference for future static scraping tasks.



## 🚀 How can it be improved

* **Headless Mode**: Configure Selenium to run in `--headless` mode for deployment on servers (AWS EC2, Linux).
* **Pagination**: Implement logic to loop through multiple pages (Page 2, 3...) to gather more data.
* **Data Persistence**: Save the scraped results into a CSV file or a Database (SQLite/PostgreSQL) for analysis.
* **Exception Handling**: Add more robust error handling for network timeouts or changes in the website's HTML structure.
* **Dynamic Keyword Search**: Allow users to input different job titles (e.g., via CLI arguments) instead of hardcoding "Data Engineer".


## 🏃‍♂️ How to Run

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_GITHUB_ID/job-search-bot.git](https://github.com/YOUR_GITHUB_ID/job-search-bot.git)
cd job-search-bot
```
2. Install Dependencies

```Bash
pip install -r requirements.txt
# Or manually:
pip install selenium beautifulsoup4 webdriver-manager requests
```

3. Run the Scraper (Selenium Version)
This will launch a Chrome window and start scraping.

```Bash
python scout.py
```

(Optional) Check the Archived Request-based Script
To see the study log of the requests method (Session/Cookie handling):
```Bash
python scout_old.py
```

---

Author: Hyomin (9nu5)

Status: Active 🟢
