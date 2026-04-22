import requests
from bs4 import BeautifulSoup
import csv
import random

URL = "https://www.avito.ru/moskva"

HEADERS = [
    "Mozilla/5.0",
    "Chrome/120.0",
    "Safari/537.36"
]

def get_html(url):
    headers = {
        "User-Agent": random.choice(HEADERS)
    }
    response = requests.get(url, headers=headers)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", {"data-marker": "item"})

    results = []

    for item in items:
        title = item.find("h3")
        price = item.find("meta", {"itemprop": "price"})
        link = item.find("a", {"data-marker": "item-title"})

        if title and price and link:
            results.append({
                "title": title.text.strip(),
                "price": price["content"],
                "link": "https://www.avito.ru" + link["href"]
            })

    return results


def save(data):
    with open("data/avito.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "price", "link"])

        for row in data:
            writer.writerow([row["title"], row["price"], row["link"]])


def main():
    html = get_html(URL)
    data = parse(html)
    save(data)
    print(f"Собрано объявлений: {len(data)}")


if __name__ == "__main__":
    main()
