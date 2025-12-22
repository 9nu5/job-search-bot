import requests
from bs4 import BeautifulSoup


def scout_green():
    url = "https://www.green-japan.com/search"

    # Query Parameters
    params = {"keyword": "データエンジニア"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params=params, headers=headers)
    print(f"Request address : {response.url}")

    if response.status_code == 200:
        print("Connection Successful!")
        print(f"response code : {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # 1, 일단 모든 박스를 타겟으로
        all_boxes = soup.find_all("div", class_=lambda x: x and "MuiBox-root" in x)
        real_job_cards = []

        # 2. aria-label 이용하여 real_job_cards 솎아내기
        for box in all_boxes:
            job_type_tag = box.find(
                # 2-1. find "募集職種" aria label
                attrs={"aria-label": "募集職種"}
            )

            # 2-2. job tag exists && 'データエンジニア' included
            if job_type_tag:
                full_text = job_type_tag.find_parent().text

                if "データエンジニア" in full_text:
                    real_job_cards.append(box)

        print(f"job cards found : {len(real_job_cards)}")

        # 3. extract data
        for i, card in enumerate(real_job_cards):
            print("\n----공고----")

            # 3-1. title
            title_tag = card.find("h2", class_=lambda x: x and "job-offer-name" in x)
            title = title_tag.text.strip() if title_tag else "無題"

            # 3-2. Find company name in ".MuiTypography-subtitle2"
            try:
                company = card.select(".MuiTypography-subtitle2")[0].text.strip()
            except:
                company = "failed to retrieve company"

            # 3-3. get info from aria-label
            def get_info(label):
                aria_label = card.find(attrs={""})
                if aria_label:
                    p_tag = aria_label.find("p")
                    if p_tag:
                        return p_tag.text.strip()
                    else:
                        return aria_label.text.strip()
                else:
                    return "-"

            location = get_info("勤務地")
            salary = get_info("想定年収")
            languages = get_info("関連スキル")

            print(f"🏢 Company: {company}")
            print(f"📜 Title: {title}")
            print(f"💰 Salary: {salary}")
            print(f"📍 Location: {location}")
            print(f"💻 Programming language: {languages}")

    else:
        print(f"Request failed : {response.status_code}")


if __name__ == "__main__":
    scout_green()
