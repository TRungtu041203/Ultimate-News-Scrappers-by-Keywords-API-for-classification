# Vietnamese Gaming News Scraper 🎮

A comprehensive web scraping pipeline for collecting and processing Vietnamese gaming news articles from multiple sources using both Selenium and traditional HTML parsing techniques.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Scraping Technologies](#scraping-technologies)
- [Supported News Sources](#supported-news-sources)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Analysis Categories](#analysis-categories)
- [Contributing](#contributing)

## 🎯 Overview

This project provides a complete solution for collecting and processing Vietnamese gaming news articles. It includes specialized web scrapers for major Vietnamese news websites, utilizing both Selenium WebDriver for dynamic content and BeautifulSoup for static HTML parsing, along with automated categorization using AI models.

## ✨ Features

- **🕷️ Multi-Source Web Scraping**: Automated scraping from 6+ Vietnamese news sources
- **🌐 Dual Scraping Approach**: Selenium WebDriver for dynamic content and HTML parsing for static sites
- **🤖 AI-Powered Categorization**: Article classification using GPT and LLaMA models
- **🔧 Flexible Configuration**: YAML-based configuration for easy customization
- **📈 Data Processing Pipeline**: Complete ETL pipeline for news data
- **🎯 Gaming Focus**: Specialized for Vietnamese gaming industry coverage
- **⚡ Optimized Performance**: Smart selection of scraping method based on website requirements

## 📁 Project Structure

```
vietnews/
├── Scrap/                          # Web scraping modules
│   ├── configs/                    # Scraper configurations
│   ├── flexible_scraper.py         # Universal scraper framework
│   ├── scrape_tinhte.py           # TinhTe.vn scraper (Selenium)
│   ├── scrape_gamek.py            # GameK scraper (HTML parsing)
│   ├── scrape_viresa.py           # Viresa scraper (HTML parsing)
│   ├── scrape_motgame.py          # MotGame scraper (Selenium)
│   ├── scrape_cafef.py            # CafeF scraper (HTML parsing)
│   └── scrape_vnex.py             # VnExpress scraper (HTML parsing)
├── classified_data/                # Categorized articles
├── cleaned_dataset/                # Processed datasets
├── Categorize_GPT.py              # GPT-based categorization
├── Categorize_Llama.py            # LLaMA-based categorization
├── post_processing.py             # Data cleaning and processing
├── merge.py                       # Data merging utilities
├── remove_dup.py                  # Duplicate removal
├── final_data.csv                 # Final processed dataset
└── README.md                      # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Git
- Chrome/Chromium browser (for Selenium scrapers)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vietnews.git
   cd vietnews
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Selenium WebDriver**
   ```bash
   # Install ChromeDriver (automatic management)
   pip install webdriver-manager
   
   # Or download ChromeDriver manually and add to PATH
   # https://chromedriver.chromium.org/
   ```

4. **Install additional dependencies for AI categorization**
   ```bash
   # For GPT categorization
   pip install openai

   # For LLaMA categorization
   pip install llama-index transformers torch
   ```

## 🚀 Usage

### Web Scraping

#### Using Flexible Scraper
```bash
python Scrap/flexible_scraper.py --config Scrap/configs/dantri.yaml --keywords "game,esports" --output-dir output
```

#### Using Specific Scrapers

**Selenium-based scrapers** (for dynamic content):
```bash
# Scrape TinhTe (requires Selenium for dynamic loading)
python Scrap/scrape_tinhte.py

# Scrape MotGame (JavaScript-heavy content)
python Scrap/scrape_motgame.py
```

**HTML parsing scrapers** (for static content):
```bash
# Scrape GameK (static HTML content)
python Scrap/scrape_gamek.py

# Scrape VnExpress (server-side rendered)
python Scrap/scrape_vnex.py

# Scrape CafeF (traditional HTML structure)
python Scrap/scrape_cafef.py
```

### Data Processing

1. **Remove duplicates**
   ```bash
   python remove_dup.py
   ```

2. **Merge datasets**
   ```bash
   python merge.py
   ```

3. **Post-process data**
   ```bash
   python post_processing.py
   ```

### AI Categorization

#### Using GPT
```bash
python Categorize_GPT.py
```

#### Using LLaMA
```bash
python Categorize_Llama.py
```

## ⚙️ Configuration

### Scraper Configuration

Create YAML configuration files in `Scrap/configs/` directory:

```yaml
site_name: example_site
base_url: https://example.com/
search_url_pattern: https://example.com/search?q={keyword}&page={page}
scraping_method: "selenium"  # or "html_parsing"

selectors:
  search:
    article_container:
      tag: article
      class: article-item
    title:
      tag: h3
      class: article-title
    # ... other selectors
```

### Environment Variables

Set up your API keys:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export LLAMA_API_KEY="your-llama-api-key"
```

## 🌐 Scraping Technologies

### Selenium WebDriver
Used for websites with **dynamic content** that requires JavaScript execution:

- **TinhTe.vn**: Dynamic article loading and infinite scroll
- **MotGame**: JavaScript-rendered content and AJAX requests
- **Complex SPA sites**: Single-page applications with client-side routing

**Features:**
- Real browser automation
- JavaScript execution
- Dynamic content loading
- User interaction simulation
- Cookie and session handling

### HTML Parsing (BeautifulSoup)
Used for websites with **static content** that can be parsed directly:

- **GameK**: Server-side rendered HTML
- **VnExpress**: Traditional website structure
- **CafeF**: Static HTML with clear tag structure
- **Viresa**: Simple HTML layout

**Features:**
- Faster execution
- Lower resource usage
- Direct HTML tag parsing
- CSS selector support
- Reliable for static content

### Technology Selection Criteria

| Website Type | Technology | Use Case |
|-------------|------------|----------|
| Dynamic/SPA | Selenium | JavaScript-heavy, AJAX loading, infinite scroll |
| Static HTML | BeautifulSoup | Server-rendered, stable HTML structure |
| Hybrid | Flexible Scraper | Configurable based on website requirements |

## 🔄 Data Processing Pipeline

1. **Data Collection**: 
   - Selenium scrapers handle dynamic content
   - HTML parsers extract from static pages
2. **Deduplication**: Remove duplicate articles using `remove_dup.py`
3. **Data Merging**: Combine datasets using `merge.py`
4. **AI Categorization**: Classify articles using GPT or LLaMA models
5. **Post-processing**: Clean and format final dataset using `post_processing.py`

## 📰 Supported News Sources

| Source | Technology | Content Type | Features |
|--------|------------|--------------|----------|
| **TinhTe.vn** | Selenium | Dynamic | Technology and gaming news with lazy loading |
| **GameK** | HTML Parsing | Static | Gaming-focused news portal with clear structure |
| **Viresa** | HTML Parsing | Static | Gaming and esports coverage |
| **MotGame** | Selenium | Dynamic | Mobile gaming news with JavaScript rendering |
| **CafeF** | HTML Parsing | Static | Business and gaming industry news |
| **VnExpress** | HTML Parsing | Static | General news with gaming section |
| **DanTri** | HTML Parsing | Static | Technology and gaming coverage |

## 🏷️ Analysis Categories

Articles are automatically categorized into:

1. **Tổng quan ngành video games tại Việt Nam** - Overview of Vietnam's gaming industry
2. **Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường** - Game development, green gaming, and environmental protection
3. **Việc phát triển games và sử dụng công cụ AIs** - Game development and AI tools usage
4. **Esports in Vietnam** - Vietnamese esports scene

## 🔧 Advanced Usage

### Custom Scraper Development

Extend the flexible scraper framework:

```python
from Scrap.flexible_scraper import FlexibleScraper

# For HTML parsing
config = {
    'base_url': 'https://newsite.com',
    'search_url_pattern': 'https://newsite.com/search?q={keyword}',
    'scraping_method': 'html_parsing',
    'selectors': {
        # Define your selectors
    }
}

# For Selenium scraping
config_selenium = {
    'base_url': 'https://dynamicsite.com',
    'search_url_pattern': 'https://dynamicsite.com/search?q={keyword}',
    'scraping_method': 'selenium',
    'wait_elements': ['article', '.content-loader'],
    'selectors': {
        # Define your selectors
    }
}

scraper = FlexibleScraper(config)
articles = scraper.crawl(['gaming', 'esports'])
```

### Selenium Configuration

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
```

## 📈 Performance Considerations

### Selenium Scrapers
- **Slower execution** but handles dynamic content
- **Higher resource usage** (RAM, CPU)
- **Rate limiting** essential to avoid detection
- **Headless mode** recommended for production

### HTML Parsing Scrapers
- **Faster execution** for static content
- **Lower resource usage**
- **Simple rate limiting** sufficient
- **Robust error handling** for network issues

### Best Practices
- Use **HTML parsing** when possible for better performance
- Implement **smart delays** between requests
- **Cache responses** to avoid duplicate requests
- **Monitor resource usage** especially for Selenium

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Happy Scraping! 🕷️📰** 
