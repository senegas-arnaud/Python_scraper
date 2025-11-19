import urllib.request
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
from functions.explore_category import explore_category


BASE_URL = "https://books.toscrape.com/"


# Explore the main website page by finding all categories and exploring each one
def explore_website():
    with urllib.request.urlopen(BASE_URL) as response:
        html = response.read().decode("utf-8")

    #Find all category URLs
    categories = re.findall( r'<a href="(catalogue/category/books/[^"]+/index.html)">', html)
    categories_urls = [BASE_URL + c for c in categories]

    categories_urls = categories_urls[:3]  # For testing purposes, limit to first 3 categories

    # Explore each category
    for category_url in categories_urls:
        explore_category(category_url)