import os
import csv
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. List of keywords to search for
keywords = [
    "trò chơi điện tử",
    "công ty game",
    "nhà phát hành game",
    "nhà lập trình game",
    "nhà làm game",
    "thiết kế game"
]

def init_browser():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    return webdriver.Chrome(service=service, options=options)

def get_tinhte_search_results(driver, keyword, max_pages=10):
    """
    Search Tinhte.vn via the embedded Google CSE overlay, paginate up to max_pages,
    and return a list of {Title_search, Summary_search, Link}.
    """
    results = []
    try:
        driver.get("https://tinhte.vn/")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "gsc-i-id1")))

        # 1) Enter keyword into the Google CSE input
        inp = driver.find_element(By.ID, "gsc-i-id1")
        inp.clear()
        inp.send_keys(keyword, Keys.RETURN)

        # 2) Wait for results overlay
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.gsc-results-wrapper-visible")))
        time.sleep(2)  # Initial wait for results

        page_count = 0
        seen_links = set()  # To avoid duplicates

        while page_count < max_pages:
            try:
                # Wait for results to load
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc-webResult")))
                time.sleep(2)  # Wait for dynamic content

                soup = BeautifulSoup(driver.page_source, "html.parser")
                items = soup.select("div.gsc-webResult")
                
                if not items:
                    print(f"No more results found for {keyword} after page {page_count}")
                    break

                new_items_found = False
                for it in items:
                    title_el = it.select_one(".gs-title a")
                    snippet_el = it.select_one("div.gsc-thumbnail-inside")
                    
                    if not title_el:
                        continue
                        
                    link = title_el.get("href", "")
                    if not link or link in seen_links:
                        continue
                        
                    seen_links.add(link)
                    new_items_found = True
                    
                    results.append({
                        "Title_search": title_el.get_text(strip=True),
                        "Summary_search": snippet_el.get_text(strip=True) if snippet_el else "",
                        "Link": link
                    })

                if not new_items_found:
                    print(f"No new items found for {keyword} after page {page_count}")
                    break

                # Try to find and click the next button
                try:
                    # Wait for pagination to be present
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gsc-cursor")))
                    
                    # Find all page numbers
                    page_numbers = driver.find_elements(By.CLASS_NAME, "gsc-cursor-page")
                    
                    # Current page is usually marked with a specific class
                    current_page = next((p for p in page_numbers if 'gsc-cursor-current-page' in p.get_attribute("class")), None)
                    
                    if current_page:
                        current_index = page_numbers.index(current_page)
                        if current_index + 1 < len(page_numbers):
                            # Click the next page number
                            next_page = page_numbers[current_index + 1]
                            driver.execute_script("arguments[0].click();", next_page)
                            time.sleep(2)  # Wait for new results to load
                            page_count += 1
                            print(f"Moved to page {page_count + 1} for {keyword}")
                            continue
                
                    # If we couldn't find the next page, try the next button
                    next_button = driver.find_element(By.CSS_SELECTOR, ".gsc-cursor-next-page")
                    if next_button:
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(2)
                        page_count += 1
                        print(f"Moved to next page for {keyword} using next button")
                        continue
                        
                except Exception as e:
                    print(f"No more pages available for {keyword} after page {page_count}")
                    break
                    
            except Exception as e:
                print(f"Error on page {page_count} for {keyword}: {str(e)}")
                break

        print(f"Found {len(results)} results for {keyword}")
        return results
        
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return results

def get_article_details(url, max_retries=3):
    """
    Fetch an article via HTTP and parse title, date, and content.
    Added retry mechanism for reliability.
    """
    for attempt in range(max_retries):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }
            r = requests.get(url, headers=headers, timeout=15)  # Increased timeout
            r.raise_for_status()
            
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Try multiple selectors for each element
            h1 = (
                soup.find("h1", class_="thread-title") or
                soup.find("h1", class_="title") or
                soup.find("h1")
            )
            
            tm = (
                soup.find("time") or
                soup.find("span", class_="thread-date") or
                soup.find("span", class_="date")
            )
            
            content_el = (
                soup.find("article") or
                soup.find("div", class_="messageContent") or
                soup.find("div", class_="thread-content")
            )
            
            t = h1.get_text(strip=True) if h1 else ""
            d = tm.get_text(strip=True) if tm else ""
            c = content_el.get_text("\n", strip=True) if content_el else ""
            
            return {"Date": d, "Title_detail": t, "Summary_detail": "", "Content": c}
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1} for {url}: {str(e)}")
                time.sleep(2 * (attempt + 1))  # Exponential backoff
                continue
            print(f"Error fetching {url}: {str(e)}")
            return {"Date": "", "Title_detail": "", "Summary_detail": "", "Content": ""}

def crawl_tinhte(keywords, max_pages_per_search=10):
    driver = init_browser()
    all_articles = []
    idx = 1
    
    for kw in keywords:
        print(f"\nSearching for keyword: {kw}")
        search_results = get_tinhte_search_results(driver, kw, max_pages=max_pages_per_search)
        
        if not search_results:
            print(f"No results for {kw}")
            continue
            
        for res in search_results:
            link = res["Link"]
            if not link.startswith("http"):
                link = "https://tinhte.vn" + link
                
            details = get_article_details(link)
            title = details["Title_detail"] or res["Title_search"]
            summary = details["Summary_detail"] or res["Summary_search"]
            
            if title and (details["Content"] or summary):  # Only add if we have content
                all_articles.append({
                    "No": idx,
                    "Date": details["Date"],
                    "Title": title,
                    "Summary": summary,
                    "Content": details["Content"],
                    "Link": link
                })
                idx += 1
                print(f"Added article {idx-1}: {title[:50]}...")
            
            time.sleep(1)
    
    driver.quit()
    return all_articles

if __name__ == "__main__":
    articles = crawl_tinhte(keywords, max_pages_per_search=10)
    
    out_dir = r"D:\Data\vietnews\output"
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, f"tinhte_{stamp}.csv")
    
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["No", "Date", "Title", "Summary", "Content", "Link"])
        w.writeheader()
        for a in articles:
            w.writerow(a)
    
    print(f"\nSaved {len(articles)} articles to {path}")
