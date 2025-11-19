import re
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