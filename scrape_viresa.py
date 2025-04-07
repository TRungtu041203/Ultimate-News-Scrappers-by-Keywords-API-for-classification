import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from datetime import datetime
import json

# The JSON endpoint that returns article data
API_URL = "https://viresa.org.vn/api/news"

# Set custom headers to mimic a real browser and avoid being blocked
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/90.0.4430.93 Safari/537.36"
    )
}

# Map of category slugs to their human-readable names
CATEGORY_SLUGS = {
    "tin-trong-nuoc": "Tin trong nước",
    "hop-tac-quoc-te": "Hợp tác quốc tế",
    "su-kien-giai-dau": "Sự kiện giải đấu",
    "goc-nhin-esports": "Góc nhìn Esports"
}

def get_article_content(url: str) -> dict:
    """
    Given the final article URL (e.g. "https://viresa.org.vn/tin-trong-nuoc/<slug>"),
    fetches and parses the HTML to extract the full title and content.

    Returns a dict with 'content' and 'full_title'.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return {"content": "", "full_title": ""}

    soup = BeautifulSoup(response.text, "html.parser")

    # Collect all <p> tags with style="text-align:justify;" and join them
    content_paragraphs = soup.find_all("p", style="text-align:justify;")
    content = "\n".join(p.get_text(strip=True) for p in content_paragraphs)

    # The detail title might be in <h2 class="article-details-title">
    title_tag = soup.find("h2", class_="article-details-title")
    full_title = title_tag.get_text(strip=True) if title_tag else ""

    return {"content": content, "full_title": full_title}

def fetch_json_articles(slug: str, max_pages: int = 20) -> list:
    """
    Hits the JSON endpoint /api/news?page=&slug= to gather articles for a given category slug.
    We'll parse the JSON for each page, then store:
      - id
      - title
      - date (from 'published_at')
      - description
      - link (we'll reconstruct from category + article slug)
    """
    all_articles = []
    for page in range(1, max_pages + 1):
        url = f"{API_URL}?page={page}&slug={slug}"
        print(f"Fetching JSON page {page}: {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            break
        except json.JSONDecodeError as je:
            print(f"JSON parse error: {je}")
            break

        # data should look like: {"data": [ { ...article... }, ...]}
        articles_list = data.get("data", [])
        if not articles_list:
            # No more articles => break
            break

        for item in articles_list:
            cat_data = item.get("category", {})
            cat_slug = cat_data.get("slug", "")
            article_slug = item.get("slug", "")

            # Reconstruct the final link to the actual article page
            # Example: https://viresa.org.vn/tin-trong-nuoc/<article-slug>
            final_link = ""
            if cat_slug and article_slug:
                final_link = f"https://viresa.org.vn/{article_slug}"

            # Extract date from 'published_at' (YYYY-MM-DD)
            published_date = item.get("published_at", "")[:10]
            description = item.get("description", "")

            # Add article meta to the all_articles list
            all_articles.append({
                "id": item.get("id"),
                "title": item.get("title", ""),
                "date": published_date,
                "description": description,
                "link": final_link,
            })

        time.sleep(2)  # Polite delay

    return all_articles

def crawl_viresa_api():
    """
    Master function:
      - For each category, fetch JSON articles
      - Then parse full content from each article webpage
    """
    all_data = []
    count = 1

    for slug, cat_name in CATEGORY_SLUGS.items():
        print(f"\n=== CATEGORY: {cat_name} ===")
        articles_json = fetch_json_articles(slug, max_pages=20)

        # For each article item from JSON, fetch the HTML content if link is provided
        for art in articles_json:
            final_title = art["title"]
            content = ""

            if art["link"]:
                detail = get_article_content(art["link"])
                if detail["full_title"]:
                    final_title = detail["full_title"]
                content = detail["content"]

            # Compose the final record
            all_data.append({
                "No": count,
                "Date": art["date"],
                "Title": final_title,
                "Summary": art["description"],  # short description from JSON
                "Content": content,             # full content from HTML
                "Link": art["link"]
            })

            count += 1

    return all_data

if __name__ == "__main__":
    articles = crawl_viresa_api()

    # Prepare output directory
    output_dir = r"D:\Data\vietnews\output"
    os.makedirs(output_dir, exist_ok=True)

    # Save results to timestamped CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"viresa_api_{timestamp}.csv")

    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["No", "Date", "Title", "Summary", "Content", "Link"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in articles:
            writer.writerow(row)

    print(f"\nDone! Data saved to {csv_file}")
