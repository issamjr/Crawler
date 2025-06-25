#!/usr/bin/env python3
"""
Advanced Web Crawler Tool
Created by Issam Junior
A powerful multi-threaded web crawler for domain exploration and link extraction
"""

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import sys
import signal
import time
import json
from datetime import datetime
import os
from urllib.robotparser import RobotFileParser
import logging

# Initialize colorama for colored output
init(autoreset=True)

# ASCII Banner
BANNER = f"""{Fore.CYAN + Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗                 ║
║   ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗                ║
║   ██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝                ║
║   ██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗                ║
║   ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║                ║
║    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝                ║
║                                                                              ║
║                  🕷️  Advanced Web Crawler v2.0  🕷️                          ║
║                        Created by Issam Junior                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

# Global variables
unique_links = set()
link_queue = set()
exit_flag = False
crawl_stats = {
    'total_pages': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'start_time': None,
    'robots_txt_checked': False
}

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global exit_flag
    print(Fore.RED + "\n[!] Gracefully stopping crawler...")
    print_statistics()
    exit_flag = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def setup_logging(log_file=None):
    """Setup logging configuration"""
    if log_file:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

def check_robots_txt(base_url):
    """Check robots.txt for crawling permissions"""
    try:
        robots_url = urljoin(base_url, '/robots.txt')
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        print(Fore.YELLOW + f"[*] Checked robots.txt: {robots_url}")
        crawl_stats['robots_txt_checked'] = True
        return rp
    except Exception as e:
        print(Fore.YELLOW + f"[!] Could not fetch robots.txt: {e}")
        return None

def fetch_page(url, timeout=10, user_agent=None):
    """Enhanced page fetching with better error handling"""
    headers = {
        'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        status_code = response.status_code
        page_size = len(response.content)
        content_type = response.headers.get('content-type', '').lower()
        
        crawl_stats['total_pages'] += 1
        if status_code == 200:
            crawl_stats['successful_requests'] += 1
        else:
            crawl_stats['failed_requests'] += 1
            
        return response.text, status_code, page_size, content_type
    except requests.exceptions.Timeout:
        print(Fore.RED + f"[!] Timeout fetching {url}")
        crawl_stats['failed_requests'] += 1
        return None, 408, None, None
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Error fetching {url}: {e}")
        crawl_stats['failed_requests'] += 1
        return None, None, None, None

def extract_links(url, base_domain, robots_parser=None, max_depth=None, current_depth=0):
    """Enhanced link extraction with depth control and robots.txt respect"""
    if max_depth is not None and current_depth >= max_depth:
        return set()
        
    if robots_parser and not robots_parser.can_fetch('*', url):
        print(Fore.YELLOW + f"[!] Robots.txt disallows crawling: {url}")
        return set()
    
    html, status_code, page_size, content_type = fetch_page(url)
    if html is None:
        return set()
    
    # Only parse HTML content
    if content_type and 'text/html' not in content_type:
        print(Fore.YELLOW + f"[!] Skipping non-HTML content: {url}")
        return set()
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    # Extract links from various tags
    for tag in soup.find_all(['a', 'link'], href=True):
        link = urljoin(url, tag['href'])
        parsed_link = urlparse(link)
        
        # Only include links from the same domain
        if parsed_link.netloc == base_domain and link not in unique_links:
            # Filter out unwanted file types
            if not any(link.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.gif', '.css', '.js', '.ico']):
                links.add(link)
    
    # Color coding based on status
    status_color = Fore.GREEN if status_code == 200 else Fore.YELLOW if status_code < 400 else Fore.RED
    size_color = Fore.CYAN
    depth_info = f" [Depth: {current_depth}]" if max_depth else ""
    
    print(f"{Fore.BLUE}[+] {url} {status_color}[{status_code}] {size_color}({page_size} bytes){depth_info}")
    
    # Log to file if logging is enabled
    logging.info(f"Crawled: {url} - Status: {status_code} - Size: {page_size} bytes")
    
    return links

def crawl_page(url, max_threads, base_domain, robots_parser=None, max_depth=None, delay=0):
    """Enhanced crawling with depth control and rate limiting"""
    global link_queue
    unique_links.add(url)
    link_queue.add(url)
    current_depth = 0
    
    while link_queue and not exit_flag:
        if max_depth is not None and current_depth >= max_depth:
            print(Fore.YELLOW + f"[*] Reached maximum depth: {max_depth}")
            break
            
        current_links = list(link_queue)
        link_queue.clear()
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {
                executor.submit(extract_links, link, base_domain, robots_parser, max_depth, current_depth): link 
                for link in current_links
            }
            
            for future in as_completed(futures):
                if exit_flag:
                    break
                    
                new_links = future.result()
                for new_link in new_links:
                    if new_link not in unique_links:
                        unique_links.add(new_link)
                        link_queue.add(new_link)
                
                # Rate limiting
                if delay > 0:
                    time.sleep(delay)
        
        current_depth += 1
        if link_queue:
            print(Fore.MAGENTA + f"[*] Moving to depth {current_depth}, {len(link_queue)} new links found")

def save_results(output_file, format_type='txt'):
    """Save results in different formats"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if format_type.lower() == 'json':
        data = {
            'timestamp': timestamp,
            'statistics': crawl_stats,
            'links': list(unique_links)
        }
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)
    else:
        with open(output_file, 'w') as file:
            file.write(f"# Web Crawler Results\n")
            file.write(f"# Generated on: {timestamp}\n")
            file.write(f"# Total links found: {len(unique_links)}\n\n")
            file.write('\n'.join(sorted(unique_links)))
    
    print(Fore.GREEN + f"[+] Results saved to {output_file}")

def print_statistics():
    """Print crawling statistics"""
    if crawl_stats['start_time']:
        duration = time.time() - crawl_stats['start_time']
        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*60)
        print(Fore.CYAN + Style.BRIGHT + "                    CRAWLING STATISTICS")
        print(Fore.CYAN + Style.BRIGHT + "="*60)
        print(Fore.GREEN + f"[+] Total unique links found: {len(unique_links)}")
        print(Fore.GREEN + f"[+] Total pages processed: {crawl_stats['total_pages']}")
        print(Fore.GREEN + f"[+] Successful requests: {crawl_stats['successful_requests']}")
        print(Fore.RED + f"[!] Failed requests: {crawl_stats['failed_requests']}")
        print(Fore.YELLOW + f"⏱️  Total crawling time: {duration:.2f} seconds")
        if crawl_stats['total_pages'] > 0:
            print(Fore.YELLOW + f"[*] Average speed: {crawl_stats['total_pages']/duration:.2f} pages/second")
        print(Fore.CYAN + Style.BRIGHT + "="*60)

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="🕷️ Advanced Web Crawler - A powerful multi-threaded crawler for domain exploration",
        epilog=f"""
Examples:
  {Fore.GREEN}python crawler.py https://example.com{Style.RESET_ALL}
  {Fore.GREEN}python crawler.py https://example.com --threads 20 --depth 3{Style.RESET_ALL}
  {Fore.GREEN}python crawler.py https://example.com -o results.json --format json --delay 1{Style.RESET_ALL}
  {Fore.GREEN}python crawler.py https://example.com --log crawler.log --no-robots{Style.RESET_ALL}
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("url", help=" The starting URL to crawl")
    parser.add_argument("--threads", type=int, default=10, 
                       help=" Number of concurrent threads (default: 10)")
    parser.add_argument("-o", "--output", 
                       help=" Save extracted links to a file")
    parser.add_argument("--format", choices=['txt', 'json'], default='txt',
                       help=" Output format: txt or json (default: txt)")
    parser.add_argument("--depth", type=int, 
                       help=" Maximum crawling depth (unlimited if not specified)")
    parser.add_argument("--delay", type=float, default=0,
                       help="  Delay between requests in seconds (default: 0)")
    parser.add_argument("--timeout", type=int, default=10,
                       help=" Request timeout in seconds (default: 10)")
    parser.add_argument("--user-agent", 
                       help=" Custom User-Agent string")
    parser.add_argument("--log", 
                       help=" Log file for detailed crawling information")
    parser.add_argument("--no-robots", action="store_true",
                       help=" Ignore robots.txt restrictions")
    
    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(Fore.RED + "[!] Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    # Setup logging
    if args.log:
        setup_logging(args.log)
    
    # Initialize statistics
    crawl_stats['start_time'] = time.time()
    
    base_domain = urlparse(args.url).netloc
    print(Fore.CYAN + Style.BRIGHT + f" Starting crawler for domain: {base_domain}")
    print(Fore.YELLOW + f" Configuration: {args.threads} threads, {args.timeout}s timeout")
    if args.depth:
        print(Fore.YELLOW + f" Maximum depth: {args.depth}")
    if args.delay:
        print(Fore.YELLOW + f" Delay between requests: {args.delay}s")
    print(Fore.CYAN + "="*60)
    
    # Check robots.txt
    robots_parser = None
    if not args.no_robots:
        robots_parser = check_robots_txt(args.url)
    
    # Start crawling
    try:
        crawl_page(
            args.url, 
            max_threads=args.threads, 
            base_domain=base_domain,
            robots_parser=robots_parser,
            max_depth=args.depth,
            delay=args.delay
        )
    except KeyboardInterrupt:
        pass
    
    # Print results
    print_statistics()
    
    print(Fore.YELLOW + Style.BRIGHT + f"\n[+] All unique links found ({len(unique_links)}):")
    for i, link in enumerate(sorted(unique_links), 1):
        print(Fore.BLUE + f"  {i:3d}. {link}")
    
    # Save results
    if args.output:
        save_results(args.output, args.format)
        print(Fore.GREEN + f"[√] Results saved to {args.output} ({args.format.upper()} format)")

if __name__ == "__main__":
    main()
