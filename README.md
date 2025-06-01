# Vietnamese Gaming News Analysis 🎮

A comprehensive data analysis pipeline for scraping, processing, and categorizing Vietnamese gaming news articles from multiple sources.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Supported News Sources](#supported-news-sources)
- [Analysis Categories](#analysis-categories)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides a complete solution for collecting, processing, and analyzing Vietnamese gaming news articles. It includes web scrapers for major Vietnamese news websites, automated categorization using AI models, and data analysis tools.

## ✨ Features

- **🕷️ Multi-Source Web Scraping**: Automated scraping from 6+ Vietnamese news sources
- **🤖 AI-Powered Categorization**: Article classification using GPT and LLaMA models
- **📊 Data Analysis**: Comprehensive analysis and visualization tools
- **🔧 Flexible Configuration**: YAML-based configuration for easy customization
- **📈 Data Processing Pipeline**: Complete ETL pipeline for news data
- **🎯 Gaming Focus**: Specialized for Vietnamese gaming industry coverage

## 📁 Project Structure

```
vietnews/
├── Scrap/                          # Web scraping modules
│   ├── configs/                    # Scraper configurations
│   ├── flexible_scraper.py         # Universal scraper framework
│   ├── scrape_tinhte.py           # TinhTe.vn scraper
│   ├── scrape_gamek.py            # GameK scraper
│   ├── scrape_viresa.py           # Viresa scraper
│   ├── scrape_motgame.py          # MotGame scraper
│   ├── scrape_cafef.py            # CafeF scraper
│   └── scrape_vnex.py             # VnExpress scraper
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

3. **Install additional dependencies for AI categorization**
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
```bash
# Scrape TinhTe
python Scrap/scrape_tinhte.py

# Scrape GameK
python Scrap/scrape_gamek.py
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

## 🔄 Data Processing Pipeline

1. **Data Collection**: Web scrapers collect articles from multiple sources
2. **Deduplication**: Remove duplicate articles using `remove_dup.py`
3. **Data Merging**: Combine datasets using `merge.py`
4. **AI Categorization**: Classify articles using GPT or LLaMA models
5. **Post-processing**: Clean and format final dataset using `post_processing.py`
6. **Analysis**: Generate insights and visualizations

## 📰 Supported News Sources

- **TinhTe.vn** - Technology and gaming news
- **GameK** - Gaming-focused news portal
- **Viresa** - Gaming and esports coverage
- **MotGame** - Mobile gaming news
- **CafeF** - Business and gaming industry news
- **VnExpress** - General news with gaming section
- **DanTri** - Technology and gaming coverage

## 🏷️ Analysis Categories

Articles are automatically categorized into:

1. **Tổng quan ngành video games tại Việt Nam** - Overview of Vietnam's gaming industry
2. **Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường** - Game development, green gaming, and environmental protection
3. **Việc phát triển games và sử dụng công cụ AIs** - Game development and AI tools usage
4. **Esports in Vietnam** - Vietnamese esports scene

## 📊 Data Analysis Features

- **Category Distribution Analysis**: Understand content distribution across categories
- **Source Analysis**: Identify most active news sources
- **Trend Analysis**: Track gaming industry trends over time
- **Word Cloud Generation**: Visualize most common terms
- **Interactive Dashboards**: Explore data with interactive visualizations

## 🔧 Advanced Usage

### Custom Scraper Development

Extend the flexible scraper framework:

```python
from Scrap.flexible_scraper import FlexibleScraper

config = {
    'base_url': 'https://newsite.com',
    'search_url_pattern': 'https://newsite.com/search?q={keyword}',
    'selectors': {
        # Define your selectors
    }
}

scraper = FlexibleScraper(config)
articles = scraper.crawl(['gaming', 'esports'])
```

### Custom Categorization

Implement your own categorization logic:

```python
def custom_categorize(article_text):
    # Your categorization logic here
    return category

# Apply to dataset
df['Custom_Category'] = df['Content'].apply(custom_categorize)
```

## 📈 Performance Considerations

- **Rate Limiting**: Built-in delays between requests to respect server resources
- **Caching**: Implements smart caching to avoid duplicate requests
- **Error Handling**: Robust error handling for network issues
- **Parallel Processing**: Support for concurrent scraping (use with caution)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Vietnamese gaming news websites for providing valuable content
- Open-source community for excellent libraries and tools
- Contributors who help improve this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/vietnews/issues) page
2. Create a new issue with detailed description
3. Contact the maintainers

## 🚨 Disclaimer

This tool is for educational and research purposes. Please respect the robots.txt files and terms of service of the websites you scrape. Be responsible and ethical in your data collection practices.

---

**Happy Analyzing! 🎮📊** 
