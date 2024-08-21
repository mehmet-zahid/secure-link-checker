import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from loguru import logger


def get_base_url(link):
    parsed_url = urlparse(link)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def extract_urls(url):
    logger.info(f"Extracting URLs from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("http"):
            urls.append(href)
    logger.info(f"Extracted {len(urls)} URLs")
    urls = list(set([get_base_url(url) for url in urls]))
    logger.info(f"Filtered URLs: (Removed duplicate domains): {len(urls)}")
    return list(urls)
