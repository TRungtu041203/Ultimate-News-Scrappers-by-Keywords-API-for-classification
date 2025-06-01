import requests
import os
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# 1. List of keywords to search for
keywords = [
    "trò chơi điện tử", 
    "công ty game",
    "nhà phát hành game",
    "nhà lập trình game",
    "nhà làm game",
    "thiết kế game"
]

# 2. Set up headers to mimic a browser (helps avoid being blocked)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.93 Safari/537.36"
    )
}

def get_search_results_page(keyword, page=1):
    """
    Given a keyword, perform a search on Cafef and return a list of articles (with title, summary, link)
    for the specified page number.
    """
    # Construct the search URL with the page parameter.
    search_url = f"https://cafef.vn/tim-kiem.chn?keywords={keyword}&page={page}"
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results for keyword '{keyword}' on page {page}: {e}")
        return []  # Return an empty list if there's an error

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="item")
    
    results = []
    for art in articles:
        # Extract title from <h3>
        title_tag = art.find("h3")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        
        # Extract link from the <a> tag within the title tag
        link_tag = title_tag.find("a")
        link = link_tag["href"] if link_tag else ""
        link = f"https://cafef.vn{link}"  # Append base URL
        
        # Extract summary from <p class="sapo">
        summary_tag = art.find("p", class_="sapo")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        results.append({
            "Title": title,
            "Summary": summary,
            "Link": link
        })
    
    return results

def get_all_search_results(keyword, max_pages=10):
    """
    Fetch search results for a given keyword across multiple pages.
    Loops from page 1 to max_pages or until no more articles are found.
    """
    all_results = []
    for page in range(1, max_pages + 1):
        print(f"Getting page {page} for keyword '{keyword}'...")
        page_results = get_search_results_page(keyword, page=page)
        if not page_results:
            print(f"No results found on page {page} for keyword '{keyword}'. Stopping.")
            break  # No more results on further pages
        all_results.extend(page_results)
        time.sleep(1)  # Polite delay between page requests
    return all_results

def get_article_details(url):
    """
    Given a link to a Cafef article, fetch and return:
    - Title (from <h1>)
    - Date (from <span class="pdate">)
    - Summary (from <h2 class="sapo">)
    - Content (from <div class="contentdetail">)
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article details from {url}: {e}")
        return {"Date": "", "Title": "", "Summary": "", "Content": ""}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract title from <h1>
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Extract summary from <h2 class="sapo">
    summary_tag = soup.find("h2", class_="sapo")
    summary = summary_tag.get_text(strip=True) if summary_tag else ""
    
    # Extract main content from <div class="contentdetail">
    content_div = soup.find("div", class_="contentdetail")
    content = content_div.get_text(separator="\n", strip=True) if content_div else ""
    
    # Extract date from <span class="pdate">
    date_tag = soup.find("span", class_="pdate")
    date = date_tag.get_text(strip=True) if date_tag else ""
    
    return {
        "Date": date,
        "Title": title,
        "Summary": summary,
        "Content": content
    }

def crawl_cafef(keywords):
    """
    Orchestrates the crawling process for Cafef:
    1. For each keyword, fetch all search results across multiple pages.
    2. For each search result, fetch detailed article data.
    3. Return a consolidated list of all articles.
    """
    all_articles = []
    count = 1
    
    for keyword in keywords:
        print(f"Searching for keyword: {keyword}")
        # Get all search results for the keyword (across multiple pages)
        search_results = get_all_search_results(keyword, max_pages=10)
        
        # For each result, fetch the full article details
        for result in search_results:
            url = result["Link"]
            if not url:
                continue
            
            article_details = get_article_details(url)
            article_data = {
                "No": count,
                "Date": article_details["Date"],
                "Title": article_details["Title"] or result["Title"],
                "Summary": article_details["Summary"] or result["Summary"],
                "Content": article_details["Content"],
                "Link": url
            }
            all_articles.append(article_data)
            count += 1
            time.sleep(1)  # Polite delay between article requests
    
    return all_articles

if __name__ == "__main__":
    # Run the crawler for all keywords
    articles = crawl_cafef(keywords)

    output_dir = r"D:\Data\vietnews\output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a unique file name with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"cafef_news_{timestamp}.csv")
    
    # Write the results to a CSV file with UTF-8 BOM encoding for Excel compatibility
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["No", "Date", "Title", "Summary", "Content", "Link"])
        writer.writeheader()
        for art in articles:
            writer.writerow(art)
    
    print(f"Data saved to {csv_file}")
    print("Crawling completed successfully.")