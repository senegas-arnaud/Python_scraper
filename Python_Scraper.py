import urllib.request
import re
import csv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://books.toscrape.com/"

def extract_data(html, url):
    data = {}
    data["product_page_url"] = url

    upc = re.search(r'<td>(.*?)</td>', html)
    data["universal_product_code"] = upc.group(1) if upc else None

    title = re.search(r'<h1>(.*?)</h1>', html)
    data["title"] = title.group(1) if title else None

    price_including_tax = re.search(r'<th>Price \(incl. tax\)</th>\s*<td>(.*?)</td>', html)
    data["price_including_tax"] = price_including_tax.group(1) if price_including_tax else None

    price_excluding_tax = re.search(r'<th>Price \(excl. tax\)</th>\s*<td>(.*?)</td>', html)
    data["price_excluding_tax"] = price_excluding_tax.group(1) if price_excluding_tax else None

    availability = re.search(r'<th>Availability</th>\s*<td>(.*?)</td>', html)
    data["availability"] = availability.group(1) if availability else None

    product_description = re.search(r'<div id="product_description" class="sub-header">\s*<h2>Product Description</h2>\s*</div>\s*<p>(.*?)</p>', html)
    data["product_description"] = product_description.group(1) if product_description else None

    review_rating = re.search(r'<p class="star-rating (.*?)">', html)
    data["review_rating"] = review_rating.group(1) if review_rating else None

    image_url = re.search(r'<div class="item active">\s*<img src="(.*?)"', html)
    data["image_url"] = BASE_URL + image_url.group(1).replace('../', '') if image_url else None

    return data

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


def main():
    with urllib.request.urlopen(BASE_URL) as response:
        html = response.read().decode("utf-8")

    categories = re.findall( r'<a href="(catalogue/category/books/[^"]+/index.html)">', html)
    categories_urls = [BASE_URL + c for c in categories]

    for category_url in categories_urls:
        explore_category(category_url)


main()
