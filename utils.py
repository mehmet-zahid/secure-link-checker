import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_base_url(link):
    parsed_url = urlparse(link)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def extract_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = set()
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("http"):
            print(href)
            urls.add(get_base_url(href))
    print(urls)
    return list(urls)
