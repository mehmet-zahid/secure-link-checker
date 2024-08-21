# Secure Link Checker

Secure Link Checker is a Flask-based web application that scans URLs for potential security threats using the VirusTotal API. It allows users to input a URL (website url), extracts domain names, and performs concurrent security scans on multiple URLs.

## Features

- Extract domain names from input website URL
- Scan multiple URLs concurrently
- Display scan results from VirusTotal
- Limit concurrent API requests to avoid rate limiting
- Dockerized application for easy deployment

## Prerequisites

- Docker and Docker Compose
- VirusTotal API key (to be set in the `.env` file)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd secure-link-checker
   ```

2. Create a `.env` file in the project root and add your VirusTotal API key:
   ```
   VIRUSTOTAL_API_KEY=your_api_key_here
   ```

3. Build and run the Docker container:
   ```
   docker compose up -d
   ```

4. Access the application at `http://localhost:5001`

## Usage

1. Open your web browser and go to `http://localhost:5001`. Port number can be changed in `compose.yml` file
2. Enter a Website URL in the provided input field
3. Click the "Check" button to initiate the scan
4. View the scan results for each extracted URL(valid unique domain)

## Project Structure

- `src/app.py`: Main Flask application file
- `src/virustotal.py`: Module for interacting with the VirusTotal API
- `src/domain_extractor.py`: Module for extracting domain names from website url
- `Dockerfile`: Instructions for building the Docker image
- `compose.yml`: Docker Compose configuration file
- `src/templates/`: Directory containing HTML templates
- `src/static/`: Directory containing static files (CSS, JS)
- `src/.env`: Environment variables file
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
- `tests/`: Directory containing test files

## Limitations

- The application is currently limited to scanning up to 10 URLs concurrently to avoid API rate limiting
- Scan results are not persisted and are generated on-demand for each request

## License

MIT License
Copyright (c) [2024] [Mehmet Zahid IŞIK]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.