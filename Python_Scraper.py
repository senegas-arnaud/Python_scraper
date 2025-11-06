import urllib.request
import re
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')


url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

with urllib.request.urlopen(url) as response:
    html = response.read().decode("utf-8")


def extract_data(html,url):
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
    data["image_url"] = "https://books.toscrape.com/" + image_url.group(1).replace('../', '') if image_url else None

    return data
#extract_data(html, url)


def explore_category(html):
    all_books = []

    while html:
        books = re.findall(r'<h3><a href="(.*?)" title="', html)
        book_url = ["https://books.toscrape.com/catalogue/" + link.replace('../', '') for link in books]
        #print(book_url)

        category = re.search(r'<title>\s*(.*?)\s*\|\s*Books to Scrape - Sandbox\s*</title>', html)
        category_name = category.group(1) if category else "Unknown"     

        for book in book_url:
            with urllib.request.urlopen(book) as response:
                book_html = response.read().decode("utf-8")
                data = extract_data(book_html, book)
                data["category"] = category_name
                all_books.append(data)

        next_page = re.search(r'<li class="next"><a href="(.*?)">next</a></li>', html)
        if next_page:
            url = "https://books.toscrape.com/catalogue/category/books/travel_2/" + next_page.group(1)
            with urllib.request.urlopen(url) as response:
                html = response.read().decode("utf-8")
        else:
            break


    with open("books_to_scrape.csv", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_books[0].keys())
        writer.writeheader()
        for book in all_books:
            writer.writerow(book)
            
    print(data)
    return book_url

explore_category(html)


    
