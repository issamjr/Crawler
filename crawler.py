import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import sys
import signal
import time

# Initialize colorama for colored output
init(autoreset=True)

# Global set to store unique links and queue for processing
unique_links = set()
link_queue = set()
exit_flag = False

def signal_handler(sig, frame):
    global exit_flag
    print(Fore.RED + "\n[!] Stopping crawler...")
    exit_flag = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        status_code = response.status_code
        page_size = len(response.content)
        return response.text, status_code, page_size
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error fetching {url}: {e}")
        return None, None, None

def extract_links(url, base_domain):
    html, status_code, page_size = fetch_page(url)
    if html is None:
        return set()
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        parsed_link = urlparse(link)
        if parsed_link.netloc == base_domain and link not in unique_links:
            links.add(link)
    
    status_color = Fore.GREEN if status_code == 200 else Fore.YELLOW if status_code < 400 else Fore.RED
    size_color = Fore.CYAN
    
    print(f"{Fore.BLUE}[+] {url} {status_color}[{status_code}] {size_color}({page_size} bytes)")
    return links

def crawl_page(url, max_threads, base_domain):
    global link_queue
    unique_links.add(url)
    link_queue.add(url)
    
    while link_queue and not exit_flag:
        current_links = link_queue.copy()
        link_queue.clear()
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {executor.submit(extract_links, link, base_domain): link for link in current_links}
            
            for future in as_completed(futures):
                if exit_flag:
                    break
                new_links = future.result()
                for new_link in new_links:
                    if new_link not in unique_links:
                        unique_links.add(new_link)
                        link_queue.add(new_link)

def main():
    parser = argparse.ArgumentParser(
        description="A powerful continuous web crawler that extracts unique links within a domain.",
        epilog="Example: python crawler.py https://example.com --threads 10 -o output.txt"
    )
    parser.add_argument("url", help="The starting URL to crawl.")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use (default: 10).")
    parser.add_argument("-o", "--output", help="Save extracted links to a file.")
    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print(Fore.RED + "[!] Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    base_domain = urlparse(args.url).netloc
    print(Fore.CYAN + Style.BRIGHT + f"[*] Starting crawler at: {args.url} (Threads: {args.threads})")
    crawl_page(args.url, max_threads=args.threads, base_domain=base_domain)

    print(Fore.YELLOW + Style.BRIGHT + "\n[*] All unique links found:")
    for link in unique_links:
        print(Fore.BLUE + f"[+] {link}")
    
    if args.output:
        with open(args.output, 'w') as file:
            file.write('\n'.join(unique_links))
        print(Fore.GREEN + f"[+] Links saved to {args.output}")

if __name__ == "__main__":
    main()

