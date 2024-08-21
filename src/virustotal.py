import requests
import base64
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

VIRUS_TOTAL_API_BASE = "https://www.virustotal.com/api/v3"

# limited api key 4 lookup per minute
VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY")

if not VIRUSTOTAL_API_KEY:
    raise ValueError("Please set the VIRUSTOTAL_API_KEY environment variable")


def scan_url(url: str) -> str | None:
    url = VIRUS_TOTAL_API_BASE + "/urls"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "application/json",
        "x-apikey": VIRUSTOTAL_API_KEY,
        "content-type": "application/x-www-form-urlencoded",
    }
    data = {"url": url}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        task_result = response.json()
        return task_result["data"]["id"]
    logger.error(f"Failed to scan URL {response.status_code} - {response.text}")
    return None


def get_result(analysis_id: str) -> dict | None:
    url = VIRUS_TOTAL_API_BASE + f"/analyses/{analysis_id}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "application/json",
        "x-apikey": VIRUSTOTAL_API_KEY,
        "content-type": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # print(result)
        stats = result["data"]["attributes"]["stats"]
        return {
            "malicious": stats["malicious"],
            "suspicious": stats["suspicious"],
            "harmless": stats["harmless"],
        }
    logger.error("Failed to get scan result")
    return None


def get_url_analysis_report(url):
    url = VIRUS_TOTAL_API_BASE + "/urls"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "application/json",
        "x-apikey": VIRUSTOTAL_API_KEY,
        "content-type": "application/json",
    }
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    url = url + "/" + url_id

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        analysis_id = result["data"]["id"]
        if not analysis_id:
            logger.error("Analysis ID not found")
            return None

        scan_result = get_result(analysis_id)
        if not scan_result:
            logger.error("Failed to get scan result")
            return None

        return scan_result

    return None


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/CAPTCHA"
    id = scan_url(url)
    print(id)
    # print(scan_result)
    print(get_result(id))
    # analysis_report = get_url_analysis_report(url)
    # print(analysis_report)
