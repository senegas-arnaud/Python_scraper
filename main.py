import urllib.request
import re
import csv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from functions.explore_website import explore_website

BASE_URL = "https://books.toscrape.com/"

def main():
    explore_website()

main()