import urllib.request
import re

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

with urllib.request.urlopen(url) as response:
    html = response.read().decode("utf-8")


def extract_data(html,url):
    data = {}
    data["product_page_url"] = url

    upc = re.search(r'<td>(.*?)</td>', html)
    data["universal_product_code"] = upc.group(1) if upc else None
    
    print(data)
    return data

extract_data(html, url)


