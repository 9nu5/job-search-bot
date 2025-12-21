import requests
from bs4 import BeautifulSoup


def scout_green():
    url = "https://www.green-japan.com/search"

    # Query Parameters
    params = {"keyword": "data engineer"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)

    print(f"Request address : {response.url}")

    if response.status_code == 200:
        print("Connection Successful!")
        print(f"response code : {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_=lambda x: x and "MuiBox-root" in x)

        if job_cards:
            print(f"📦 Job cards found: {len(job_cards)}")

            for i in range(min(3, len(job_cards))):
                card = job_cards[1]
                print(f"\n {i} checked")
                candidates = card.select(".MuiTypography-subtitle2")

                if candidates:
                    print(f"candidates found : {len(candidates)}")
                    for idx, item in enumerate(candidates):
                        print(f"candidate [{idx}]:{item.text.strip()}")
                else:
                    print("No candidates found.")
                    print(f"{card.prettify()[:100]}...")
        else:
            print("No job cards found.")

    else:
        print(f"Request failed : {response.status_code}")


if __name__ == "__main__":
    scout_green()
