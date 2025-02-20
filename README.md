# Crawler
Continuous Web Crawler
## Description
Enhanced Web Crawler is a powerful and efficient web crawler designed to continuously extract unique links within a given domain. The crawler avoids revisiting links, displays HTTP status codes and page sizes in different colors, and allows customization of thread usage. It runs indefinitely until all links have been processed or the user manually stops it with `CTRL + C`.

## Features
- **Continuous Crawling:** The crawler runs indefinitely, exploring all links within the same domain until no new links are found.
- **Multi-threaded Processing:** Uses concurrent requests to improve crawling efficiency.
- **Smart URL Filtering:** Ensures only links from the given domain are processed.
- **Colored Output:** Displays HTTP status codes and page sizes in different colors.
- **Graceful Exit Handling:** Stops cleanly when `CTRL + C` is pressed.
- **Output to File:** Saves extracted links if the `-o` option is used.

## Installation
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
Run the crawler with the following command:
```bash
python crawler.py <URL> [--threads THREADS] [-o OUTPUT_FILE]
```

### Arguments:
- `<URL>`: The starting URL for crawling.
- `--threads THREADS`: (Optional) Number of threads to use (default is 10).
- `-o OUTPUT_FILE`: (Optional) Save extracted links to a file.

### Example:
```bash
python crawler.py https://example.com --threads 10 -o links.txt
```

## Requirements
- Python 3.x
- requests
- BeautifulSoup4
- colorama

## Stopping the Crawler
To stop the crawler at any time, press `CTRL + C`.

## License
This project is open-source and available under the MIT License.

