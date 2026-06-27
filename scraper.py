import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

all_books_data = []

for page_num in range(1,5):

    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"

    print(f"Scraping page {page_num}:{url}")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Page {page_num} not found. stopping.")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    all_books_on_page = soup.find_all("article", class_="product_pod")


    for book in all_books_on_page:

        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        all_books_data.append({
            "title": title,
            "price": price,
            "rating": rating
        })

    print(f"page {page_num} scraped.waiting 1 second...")
    time.sleep(1)

with open("all_books.CSV", "w", newline="", encoding="utf-8") as file:
    headers = ["title", "price", "rating"]
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_books_data)

print(f"\nScraping complete found {len(all_books_data)} Books. Check for all_books.csv.")