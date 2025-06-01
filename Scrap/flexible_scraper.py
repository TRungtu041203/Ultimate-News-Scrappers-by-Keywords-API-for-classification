import requests
import os
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import argparse
import json
import yaml
from urllib.parse import quote_plus

class FlexibleScraper:
    def __init__(self, config):
        """
        Initialize the scraper with configuration
        config: dict containing website configuration
        """
        self.config = config
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/90.0.4430.93 Safari/537.36"
            )
        }
        self.base_url = config['base_url']
        self.search_url_pattern = config['search_url_pattern']
        self.selectors = config['selectors']

    def get_search_results_page(self, keyword, page=1):
        """Get search results for a given keyword and page number"""
        # Properly encode the keyword for URL
        encoded_keyword = quote_plus(keyword)
        search_url = self.search_url_pattern.format(
            base_url=self.base_url,
            keyword=encoded_keyword,
            page=page
        )
        
        print(f"Searching URL: {search_url}")  # Debug print
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching search results: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all(self.selectors['search']['article_container']['tag'],
                               class_=self.selectors['search']['article_container'].get('class'))
        
        print(f"Found {len(articles)} article containers on page {page}")  # Debug print
        
        results = []
        for art in articles:
            # Extract title
            title_tag = art.find(self.selectors['search']['title']['tag'],
                               class_=self.selectors['search']['title'].get('class'))
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            
            # Extract link
            link_tag = title_tag.find('a') if self.selectors['search']['link'].get('inside_title') else art.find('a')
            link = link_tag['href'] if link_tag else ""
            if link and not link.startswith('http'):
                link = f"{self.base_url.rstrip('/')}/{link.lstrip('/')}"
            
            # Extract summary
            summary_tag = art.find(self.selectors['search']['summary']['tag'],
                                 class_=self.selectors['search']['summary'].get('class'))
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            
            results.append({
                "Title_search": title,
                "Summary_search": summary,
                "Link": link
            })
        
        print(f"Successfully extracted {len(results)} articles from page {page}")  # Debug print
        return results

    def get_all_search_results(self, keyword, max_pages=10):
        """Get all search results across multiple pages"""
        all_results = []
        for page in range(1, max_pages + 1):
            print(f"Getting page {page} for keyword '{keyword}'...")
            page_results = self.get_search_results_page(keyword, page=page)
            if not page_results:
                print(f"No results found on page {page}. Stopping pagination for keyword '{keyword}'")
                break
            all_results.extend(page_results)
            time.sleep(1)
        print(f"Total articles found for keyword '{keyword}': {len(all_results)}")
        return all_results

    def get_article_details(self, url):
        """Get detailed article information"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article details: {e}")
            return {"Date": "", "Title_detail": "", "Summary_detail": "", "Content": ""}
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title
        title_tag = soup.find(self.selectors['article']['title']['tag'],
                            class_=self.selectors['article']['title'].get('class'))
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        # Extract summary
        summary_tag = soup.find(self.selectors['article']['summary']['tag'],
                              class_=self.selectors['article']['summary'].get('class'))
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        # Extract content
        content_tag = soup.find(self.selectors['article']['content']['tag'],
                              class_=self.selectors['article']['content'].get('class'))
        content = content_tag.get_text(separator="\n", strip=True) if content_tag else ""
        
        # Extract date
        date_tag = soup.find(self.selectors['article']['date']['tag'],
                           class_=self.selectors['article']['date'].get('class'))
        date = date_tag.get_text(strip=True) if date_tag else ""
        
        return {
            "Date": date,
            "Title_detail": title,
            "Summary_detail": summary,
            "Content": content
        }

    def crawl(self, keywords):
        """Main crawling function"""
        all_articles = []
        count = 1
        
        for keyword in keywords:
            print(f"Searching for keyword: {keyword}")
            search_results = self.get_all_search_results(keyword, max_pages=10)
            
            for result in search_results:
                url = result["Link"]
                if not url:
                    continue
                
                article_details = self.get_article_details(url)
                
                final_title = article_details["Title_detail"] or result["Title_search"]
                final_summary = article_details["Summary_detail"] or result["Summary_search"]
                
                article_data = {
                    "No": count,
                    "Date": article_details["Date"],
                    "Title": final_title,
                    "Summary": final_summary,
                    "Content": article_details["Content"],
                    "Link": url
                }
                all_articles.append(article_data)
                count += 1
                time.sleep(1)
        
        return all_articles

def load_config(config_file):
    """Load configuration from YAML or JSON file"""
    if config_file.endswith('.yaml') or config_file.endswith('.yml'):
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif config_file.endswith('.json'):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError("Config file must be either YAML or JSON")

def main():
    parser = argparse.ArgumentParser(description='Flexible Web Scraper')
    parser.add_argument('--config', required=True, help='Path to configuration file (YAML or JSON)')
    parser.add_argument('--keywords', required=True, help='Comma-separated list of keywords to search for')
    parser.add_argument('--output-dir', default='output', help='Output directory for CSV files')
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    
    # Initialize scraper
    scraper = FlexibleScraper(config)
    
    # Parse keywords
    keywords = [k.strip() for k in args.keywords.split(',')]
    
    # Run scraper
    articles = scraper.crawl(keywords)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    site_name = config.get('site_name', 'scraped')
    csv_file = os.path.join(args.output_dir, f"{site_name}_{timestamp}.csv")
    
    # Save results
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["No", "Date", "Title", "Summary", "Content", "Link"])
        writer.writeheader()
        for art in articles:
            writer.writerow(art)
    
    print(f"Data saved to {csv_file}")
    print("Crawling completed successfully.")

if __name__ == "__main__":
    main() 