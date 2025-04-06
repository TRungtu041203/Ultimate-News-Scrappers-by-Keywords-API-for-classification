import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.93 Safari/537.36"
    )
}

BASE_URL = "https://viresa.org.vn"

def get_initial_articles():
    url = BASE_URL
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the article list: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    article_divs = soup.select("div.articles-top") or soup.select("div.row.pb-4.flex") # matches each article container
    for div in article_divs:
        link_tag = div.find("a", href=True)
        if not link_tag:
            continue
        link = link_tag["href"]
        if not link.startswith("http"):
            link = BASE_URL + link
        title = link_tag.get_text(strip=True)

        date_tag = div.find("small")
        date = date_tag.get_text(strip=True) if date_tag else ""

        articles.append({"title": title, "link": link, "date": date})
    return articles

def get_article_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return {"content": "", "full_title": ""}

    soup = BeautifulSoup(response.text, "html.parser")

    content_div = soup.find("div", class_="content-inner")
    content = content_div.get_text(separator="\n", strip=True) if content_div else ""

    title_tag = soup.find("h1", class_="jeg_post_title")
    full_title = title_tag.get_text(strip=True) if title_tag else ""

    return {"content": content, "full_title": full_title}

def crawl_viresa_static():
    articles = get_initial_articles()
    all_data = []
    for i, art in enumerate(articles, 1):
        print(f"Crawling article {i}: {art['title']}")
        detail = get_article_content(art["link"])
        all_data.append({
            "No": i,
            "Date": art["date"],
            "Title": detail["full_title"] or art["title"],
            "Summary": "",  # not available directly
            "Content": detail["content"],
            "Link": art["link"]
        })
        time.sleep(1)
    return all_data

if __name__ == "__main__":
    articles = crawl_viresa_static()

    output_dir = r"D:\Data\vietnews\output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"viresa_static_{timestamp}.csv")

    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["No", "Date", "Title", "Summary", "Content", "Link"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for art in articles:
            writer.writerow(art)

    print(f"Saved to {csv_file}")
