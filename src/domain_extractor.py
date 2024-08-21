import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, ParseResult, urljoin
from loguru import logger


def is_valid_url(url):
    try:
        result: ParseResult = urlparse(url)
        return result.scheme in ["http", "https"] and bool(result.netloc)
    except ValueError:
        return False


def extract_domain_names(url):
    logger.info(f"Extracting domain names from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    base_url = get_base_url(url)
    domains = set()

    # Extract domain names from various HTML elements and attributes
    for tag in soup.find_all(["a", "img", "script", "link"]):
        for attr in ["href", "src", "data-src"]:
            link = tag.get(attr)
            if link:
                domain = get_domain(link, base_url)
                if domain:
                    domains.add(domain)

    logger.info(f"Extracted {len(domains)} unique domain names")
    return list(domains)


def get_domain(url, base_url):
    if not url.startswith(("http://", "https://")):
        # Check if it's a valid relative path
        if url.startswith("/") or "." in url or "/" in url:
            full_url = urljoin(base_url, url)
        else:
            return None  # Not a valid URL or relative path
    else:
        full_url = url

    if is_valid_url(full_url):
        return urlparse(full_url).netloc
    return None


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


# Example usage
if __name__ == "__main__":
    target_url = "ftp://nuxt.com"
    print(is_valid_url(target_url))
    print(get_domain(target_url, "https://example.com"))
    # extracted_domains = extract_domain_names(target_url)
    # for domain in extracted_domains:
    #    print(domain)
