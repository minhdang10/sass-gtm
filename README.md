# SaaS Security GTM Signal Tracker

A lightweight, automated data system that identifies companies actively hiring for SaaS security roles and people discussing SaaS security topics across multiple platforms.

## System Overview

This system consists of two main components:

1. **Hiring Signal Tracker**: Identifies top companies hiring for SaaS Security, SSPM, AI Agent Security, and Compliance roles
2. **Conversation Signal Tracker**: Tracks discussions about SaaS security topics on X (Twitter), Reddit, and top cybersecurity publishers

## Architecture

```
saas_security_gtm_tracker/
├── config.py              # Configuration and search terms
├── hiring_tracker.py      # Job board scraping and company identification
├── conversation_tracker.py # Social media and publisher monitoring
├── data_processor.py      # Data cleaning and ranking
├── main.py                # Main orchestration script
├── requirements.txt       # Python dependencies
├── outputs/               # Generated data files
│   ├── hiring_signals.csv
│   └── conversation_signals.csv
└── README.md
```

## Data Sources

### Hiring Signals
- **Indeed API/Scraping**: Job postings with SaaS security keywords
- **LinkedIn**: Company job postings (via web scraping with rate limiting)
- **Glassdoor**: Additional job listings

### Conversation Signals
- **X (Twitter)**: Using Twitter API v2 or web scraping
- **Reddit**: Using PRAW (Python Reddit API Wrapper)
- **Cybersecurity Publishers**: RSS feeds and web scraping from:
  1. The Hacker News
  2. Dark Reading
  3. SecurityWeek
  4. Krebs on Security
  5. Bleeping Computer
  6. Threatpost
  7. CSO Online
  8. SC Magazine
  9. InfoSecurity Magazine
  10. Security Boulevard

## Weekly Refresh Mechanism

The system supports weekly updates through:
- **Manual execution**: Run `python main.py` weekly
- **Cron job**: Configure cron to run every Monday at 9 AM
- **GitHub Actions**: Automated weekly runs (if hosted on GitHub)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

This will generate:
- `outputs/hiring_signals.csv`: Top companies hiring for SaaS security roles
- `outputs/conversation_signals.csv`: People and publishers discussing SaaS security topics

## Key Insights

The system extracts:
- Company hiring trends and growth signals
- Influential voices in SaaS security discussions
- Trending topics and breach discussions
- Publisher engagement metrics

## Known Limitations

1. **Rate Limiting**: Some APIs (LinkedIn, Twitter) have strict rate limits
2. **Data Freshness**: Web scraping may miss some recent posts
3. **Relevance Scoring**: Keyword matching may include false positives
4. **Scale**: Top 1,000 companies may require multiple data sources
5. **LinkedIn Access**: Requires creative workarounds due to API restrictions

