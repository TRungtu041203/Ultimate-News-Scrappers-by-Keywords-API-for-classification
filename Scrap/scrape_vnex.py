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

# 2. Set up headers to mimic a browser (helps avoid being blocked by some sites)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.93 Safari/537.36"
    )
}

def get_search_results_page(keyword, page =1):
    """
    Given a keyword, perform a search on VnExpress
    and return a list of articles (with title, summary, link).
    """
    # A. Construct the search URL
    #    Note: If VnExpress changes its search URL, update this pattern accordingly.
    search_url = f"https://timkiem.vnexpress.net/?q={keyword}&page={page}"
    
    # B. Request the search page
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # C. Find all article containers. (Adjust if the structure changes.)
    articles = soup.find_all("article")
    
    results = []
    for art in articles:
        # Extract title
        title_tag = art.find("h3")
        if not title_tag:
            # If we can't find a title, skip this item
            continue
        
        title = title_tag.get_text(strip=True)
        
        # Extract link
        link_tag = title_tag.find("a")
        link = link_tag["href"] if link_tag else ""
        
        # Extract summary from <p class="description">
        summary_tag = art.find("p", class_="description")
        if summary_tag:
            # Remove <span class="location-stamp"> if you don't want it in the final summary
            location_span = summary_tag.find("span", class_="location-stamp")
            if location_span:
                location_span.decompose()  # Removes the <span> entirely
            summary = summary_tag.get_text(strip=True)
        else:
            summary = ""
        
        results.append({
            "Title": title,
            "Summary": summary,
            "Link": link
        })
    
    return results

def get_all_search_results(keyword, max_pages = 10):
    all_results = []
    for page in range(1, max_pages + 1):
        print(f"Getting page {page} of search results")
        page_results = get_search_results_page(keyword, page=page)
        if not page_results:
            break  # No more results
        all_results.extend(page_results)
        
        # Be polite: short delay between requests to avoid spamming the server
        time.sleep(1)
    
    return all_results


def get_article_details(url):
    """
    Given a link to a VnExpress article, fetch and return:
    - Title
    - Date
    - Summary (from the article page)
    - Content (the full text content of the article)
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # A. Extract the article title (in <h1>)
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # B. Extract the article summary
    summary_tag = soup.find("p", class_="description")
    summary = summary_tag.get_text(strip=True) if summary_tag else ""
    
    # C. Extract the main content
    #    VnExpress uses <article class="fck_detail"> for content
    content_div = soup.find("article", class_="fck_detail")
    if content_div:
        content = content_div.get_text(separator="\n", strip=True)
    else:
        content = ""
    
    #D. Extract the dates 
    #   VNExpress 
    date_tag = soup.find("span", class_ = "date")
    date = date_tag.get_text(strip = True) if date_tag else ""

    return {
        "Date": date,
        "Title": title,
        "Summary": summary,
        "Content": content,

    }

def crawl_vnexpress(keywords):
    """
    Orchestrates the entire crawling process:
    1. For each keyword, get the search results.
    2. For each search result, fetch the full article details.
    3. Return a consolidated list of all articles.
    """
    all_articles = []
    count = 1
    
    for keyword in keywords:
        print(f"Searching for keyword: {keyword}")
        
        # 1. Get the search result list for the current keyword
        search_results = get_all_search_results(keyword, max_pages = 10)
        
        # 2. For each search result, fetch more details from the article page
        for result in search_results:
            url = result["Link"]
            if not url:
                continue  # Skip if the link is missing

            article_details = get_article_details(url)
            
            # Combine everything into one record
            article_data = {
                "No": count,
                "Date": article_details["Date"],
                # If the article page has a more accurate Title, use that.
                # Otherwise, fall back to the Title from the search result.
                "Title": article_details["Title"] or result["Title"],
                
                # Same logic for summary
                "Summary": article_details["Summary"] or result["Summary"],
                
                "Content": article_details["Content"],
                "Link": url
            }
            
            all_articles.append(article_data)
            count += 1
            
            # Be polite: short delay between requests to avoid spamming the server
            time.sleep(1)
    
    return all_articles

if __name__ == "__main__":
    # 3. Run the crawler for all keywords
    articles = crawl_vnexpress(keywords)
    
    output_dir = "D:\Data\vietnews\output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 4. Generate a unique file name with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"vnexpress_news_{timestamp}.csv"
    
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["No", "Date", "Title", "Summary", "Content", "Link"])
        writer.writeheader()
        for art in articles:
            writer.writerow(art)
    
    print(f"Data saved to {csv_file}")
