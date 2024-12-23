import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def write_urls(file_path, urls):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + "\n")

def add_to_blacklist(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    with open('./blacklist.txt', 'a') as file:
        file.write(domain + "\n")

def get_sitemap_url(url):
    if not url.endswith("/"):
        url += "/"
    return url + "sitemap.xml"

def get_sitemap_from_robots(url):
    robots_url = url + ("robots.txt" if url.endswith("/") else "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            sitemap_urls = re.findall(r"Sitemap:\s*(.*)", response.text)
            return sitemap_urls
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {robots_url} ({e})")
    return []

def guess_sitemap_urls(url):
    common_sitemap_paths = [
        "sitemap.xml",
        "sitemap_index.xml",
        "sitemap1.xml",
        "sitemap/sitemap.xml",
        "sitemap_index/sitemap.xml"
    ]
    guessed_urls = []
    for path in common_sitemap_paths:
        guessed_urls.append(url + (path if url.endswith("/") else f"/{path}"))
    return guessed_urls

def count_pages_in_sitemap(sitemap_url, depth=0, max_depth=6, max_sitemaps=50, visited_sitemaps=None):
    if visited_sitemaps is None:
        visited_sitemaps = set()
    if sitemap_url in visited_sitemaps:
        print(f"Skipping already visited sitemap: {sitemap_url}")
        return 0
    visited_sitemaps.add(sitemap_url)
    
    if depth > max_depth:
        print(f"Maximum sitemap depth reached ({max_depth}) for: {sitemap_url}")
        return 0
    try:
        print(f"Fetching sitemap: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, features='xml')
            urls = soup.find_all('loc')
            sitemaps = soup.find_all('sitemap')

            if sitemaps:
                if len(sitemaps) > max_sitemaps:
                    print(f"Too many sitemaps found ({len(sitemaps)}) for: {sitemap_url}, adding to blacklist.")
                    add_to_blacklist(sitemap_url)
                    return 0
                max_page_count = 0
                for sitemap in sitemaps:
                    sub_sitemap_url = sitemap.find('loc').text
                    print(f"Found sub-sitemap: {sub_sitemap_url}")
                    page_count = count_pages_in_sitemap(sub_sitemap_url, depth + 1, max_depth, max_sitemaps, visited_sitemaps)
                    if page_count > max_page_count:
                        max_page_count = page_count
                    if max_page_count > 50:
                        print(f"Sitemap contains more than 50 pages, stopping further exploration.")
                        return max_page_count
                print(f"Total pages in sitemap and sub-sitemaps: {max_page_count}")
                return max_page_count
            else:
                page_count = len(urls)
                print(f"Sitemap fetched successfully: {sitemap_url} contains {page_count} pages")
                return page_count
        else:
            print(f"Failed to fetch sitemap: {sitemap_url} (Status code: {response.status_code})")
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {sitemap_url} ({e})")
    return 0

def count_pages_alternative(url):
    try:
        print(f"Using alternative method to estimate page count for: {url}")
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            unique_links = set(link['href'] for link in links if link['href'].startswith('/') or link['href'].startswith(url))
            page_count = len(unique_links)
            print(f"Estimated page count for {url} is {page_count} based on internal links")
            return page_count
        else:
            print(f"Failed to fetch URL: {url} (Status code: {response.status_code})")
    except requests.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
    return 0

def filter_url(url, max_pages=50):
    print(f"Processing URL: {url}")
    sitemap_urls = [get_sitemap_url(url)]
    sitemap_urls += get_sitemap_from_robots(url)
    sitemap_urls += guess_sitemap_urls(url)
    found_pages = False
    visited_sitemaps = set()
    for sitemap_url in sitemap_urls:
        page_count = count_pages_in_sitemap(sitemap_url, visited_sitemaps=visited_sitemaps)
        if page_count > 0:
            found_pages = True
            if page_count <= max_pages:
                print(f"Keeping URL: {url} (contains {page_count} pages)")
                return url
            else:
                print(f"Removed {url}: contains {page_count} pages (> {max_pages})")
            break
    if not found_pages:
        print(f"No valid sitemap found for URL: {url}, using alternative method.")
        page_count = count_pages_alternative(url)
        if page_count > 0 and page_count <= max_pages:
            print(f"Keeping URL: {url} (contains {page_count} pages)")
            return url
        elif page_count > max_pages:
            print(f"Removed {url}: contains {page_count} pages (> {max_pages})")
        else:
            print(f"No valid pages found for URL: {url}, adding to blacklist.")
            add_to_blacklist(url)
    return None

def filter_urls(urls, max_pages=20):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda url: filter_url(url, max_pages), urls))
    return [url for url in results if url is not None]

def main():
    input_file = './final_link.txt'
    output_file = './filtered_list.txt'

    print(f"Reading URLs from {input_file}")
    urls = read_urls(input_file)
    print(f"Total URLs read: {len(urls)}")

    filtered_urls = filter_urls(urls)
    print(f"Total URLs after filtering: {len(filtered_urls)}")

    print(f"Writing filtered URLs to {output_file}")
    write_urls(output_file, filtered_urls)

    print(f"Filtered URLs saved to {output_file}")

if __name__ == "__main__":
    main()