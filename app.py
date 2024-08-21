from flask import Flask, render_template, request, jsonify
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

from virustotal import scan_url, get_result
from utils import extract_urls

CONCURRENT_REQUESTS = 10


app = Flask(__name__)


def process_url(url: str) -> dict | None:
    task_id = scan_url(url)
    if not task_id:
        logger.error(f"Failed to scan URL: {url}")
        return None

    scan_result = get_result(task_id)
    if not scan_result:
        logger.error(f"Failed to get scan result: {url}")
        return None

    return {
        "url": url,
        "scan_result": scan_result,
    }


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/url-check", methods=["POST"])
def url_check():
    try:
        url = request.form.get("url")
        if not url:
            return render_template("results.html", error="Please provide a URL")

        urls = extract_urls(url)
        if not urls:
            return render_template(
                "results.html",
                error="Could not extract any valid URLs from the provided input",
            )

        random.shuffle(urls)

        # API limitation
        original_url_count = len(urls)
        urls = urls[:CONCURRENT_REQUESTS] if len(urls) > CONCURRENT_REQUESTS else urls
        api_limited = original_url_count > CONCURRENT_REQUESTS

        results = []
        with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
            future_to_url = {executor.submit(process_url, url): url for url in urls}
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    results.append(result)

        if not results:
            return render_template(
                "results.html", error="Failed to get scan results for all URLs"
            )

    except Exception as e:
        logger.error(f"Failed to process URL: {e}")
        logger.error(f"Failed to process URL: {url}")
        return jsonify({"error": "Failed to process URL"}), 500

    return render_template(
        "results.html",
        results=results,
        api_limited=api_limited,
        original_url_count=original_url_count,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
