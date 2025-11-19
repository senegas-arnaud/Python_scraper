import urllib.request
import re
import csv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from functions.extract_data import extract_data
from functions.clear_name import clear_name
from functions.download_image_url import download_image_url


BASE_URL = "https://books.toscrape.com/"





def explore_category(category_url):
    all_books = []

    while category_url:
        with urllib.request.urlopen(category_url) as response:
            html = response.read().decode("utf-8")

        category = re.search(r'<title>\s*(.*?)\s*\|\s*Books to Scrape - Sandbox\s*</title>', html)
        category_name = category.group(1) if category else "Unknown"

        books = re.findall(r'<h3><a href="(.*?)" title="', html)
        book_urls = [BASE_URL + "catalogue/" + link.replace('../', '') for link in books]

        for book_url in book_urls:
            with urllib.request.urlopen(book_url) as response:
                book_html = response.read().decode("utf-8")
                data = extract_data(book_html, book_url)
                data["category"] = category_name
                all_books.append(data)

                if data["image_url"] and data["title"]:
                    image_folder = os.path.join("photos", clear_name(category_name))
                    os.makedirs(image_folder, exist_ok=True)
                    image_name = f"{clear_name(data['title'])}.jpg"
                    if len(image_name) > 50:
                        image_name = image_name[:50] + "... " + ".jpg"
                    download_image_url(data["image_url"], image_folder, image_name)
                else:
                    print(f"Skipping image for book '{data['title']}' (no image URL)")


        next_page = re.search(r'<li class="next"><a href="(.*?)">next</a></li>', html)
        if next_page:
            category_base = category_url.rsplit('/', 1)[0] + "/"
            category_url = category_base + next_page.group(1)
        else:
            category_url = None

    os.makedirs('.csv', exist_ok=True)

    if all_books:
        filename = os.path.join(".csv", f"{category_name.replace(' ', '_').lower()}.csv")
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=all_books[0].keys())
            writer.writeheader()
            for book in all_books:
                writer.writerow(book)

    print(f"Category '{category_name}' done with {len(all_books)} books.")