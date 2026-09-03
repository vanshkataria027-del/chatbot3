import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

BASE_URL = "https://www.abhiwan.com"

visited = set()
all_text = []


def scrape_page(url):
    if url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            print("Failed:", url)
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text:
            all_text.append(
                f"\n\nSOURCE: {url}\n{text}"
            )

        print("Scraped:", url)

        # Find links
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])

            parsed = urlparse(next_url)

            if (
                parsed.netloc == urlparse(BASE_URL).netloc
                and next_url not in visited
            ):
                scrape_page(next_url)

    except Exception as e:
        print("Error:", url, e)


scrape_page(BASE_URL)

os.makedirs("data", exist_ok=True)

with open("data/website.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print("\nDONE!")
print("Pages scraped:", len(visited))
print("Data saved in: data/website.txt")