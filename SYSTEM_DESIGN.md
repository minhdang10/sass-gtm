# System Design Overview

## Architecture

The SaaS Security GTM Tracker is designed as a modular, lightweight data pipeline that can run weekly to surface actionable GTM signals. The system follows a three-stage architecture:

```
Data Collection → Processing & Ranking → Output Generation
```

### Components

1. **Hiring Tracker** (`hiring_tracker.py`)
   - Scrapes job boards (Indeed, LinkedIn)
   - Identifies companies hiring for SaaS security roles
   - Aggregates and ranks companies by hiring activity

2. **Conversation Tracker** (`conversation_tracker.py`)
   - Monitors X (Twitter), Reddit, and cybersecurity publishers
   - Tracks discussions about SaaS security topics
   - Identifies influential voices and active publishers

3. **Data Processor** (`data_processor.py`)
   - Cleans and normalizes company names
   - Deduplicates records
   - Enriches data with metadata

4. **Main Orchestrator** (`main.py`)
   - Coordinates data collection
   - Generates CSV outputs
   - Handles error management

## Data Flow

### Hiring Signals Pipeline

```
Job Board APIs/Scraping
    ↓
Keyword-based Search (5 categories)
    ↓
Company Extraction & Aggregation
    ↓
Deduplication & Normalization
    ↓
Ranking by Signal Strength
    ↓
CSV Output (Top 1,000 companies)
```

### Conversation Signals Pipeline

```
Social Media APIs (X, Reddit)
    ↓
RSS Feeds (10 Publishers)
    ↓
Topic-based Search (7 topics)
    ↓
Author/Publisher Extraction
    ↓
Engagement Scoring
    ↓
Ranking by Influence
    ↓
CSV Output (Top 500 people + Publishers)
```

## Data Sources

### Hiring Signals

| Source | Method | Rate Limits | Coverage |
|--------|--------|-------------|----------|
| Indeed | Web Scraping | ~2 req/sec | High |
| LinkedIn | Web Scraping (Selenium) | Strict | Medium |
| Glassdoor | Web Scraping | Moderate | Medium |

**Search Categories:**
- SaaS Security
- SSPM (SaaS Security Posture Management)
- AI Agent Security
- SaaS Compliance
- AI Compliance

### Conversation Signals

| Platform | Method | Rate Limits | Coverage |
|----------|--------|-------------|----------|
| X (Twitter) | API v2 / Scraping | 300 req/15min | High |
| Reddit | PRAW API | 60 req/min | High |
| Publishers | RSS Feeds | None | High |

**Topics Tracked:**
- SaaS Security / SSPM
- SaaS Compliance
- AI Agent Security
- Salesforce breach
- Gainsight breach
- Salesloft breach

**Top 10 Publishers:**
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

### Option 1: Manual Execution
```bash
python main.py
```

### Option 2: Cron Job (Linux/Mac)
```bash
# Add to crontab (runs every Monday at 9 AM)
0 9 * * 1 cd /path/to/saas_security_gtm_tracker && python main.py
```

### Option 3: GitHub Actions
```yaml
# .github/workflows/weekly_refresh.yml
name: Weekly GTM Signal Refresh
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:  # Manual trigger
```

### Option 4: Cloud Scheduler (GCP/AWS)
- AWS EventBridge / Lambda
- Google Cloud Scheduler / Cloud Functions
- Azure Logic Apps

## Signal Quality Metrics

### Hiring Signals
- **Signal Strength**: Calculated from:
  - Number of job postings (weight: 10x)
  - Number of categories (weight: 5x)
  - Number of data sources (weight: 3x)
- **Ranking**: By total jobs, then signal strength

### Conversation Signals
- **Influence Score**: Based on:
  - Engagement metrics (likes, retweets, upvotes)
  - Post frequency
  - Topic relevance
- **Relevance Score**: Number of relevant articles/posts

## Data Output Format

### Hiring Signals CSV
- Rank
- Company Name
- Total Jobs
- Categories
- Signal Strength
- Sample Roles
- Data Sources
- Last Updated

### Conversation Signals CSV (People)
- Rank
- Username/ID
- Platform
- Engagement Score
- Influence Score
- Topics Discussed
- Number of Posts
- Sample Post
- Last Updated

### Conversation Signals CSV (Publishers)
- Rank
- Publisher Name
- Relevance Score
- Number of Articles
- Topics Covered
- Website URL
- Sample Article
- Last Updated

## Key Design Decisions

1. **Modularity**: Separate trackers for hiring and conversation signals allow independent scaling and updates

2. **Rate Limiting**: Built-in delays and session management to respect API limits

3. **Deduplication**: Company name normalization prevents duplicate entries

4. **Scalability**: Designed to handle 1,000+ companies and 500+ people with efficient data structures

5. **Extensibility**: Easy to add new data sources or search terms via configuration

## Known Limitations & Tradeoffs

1. **API Access**
   - LinkedIn: Requires partnership or careful scraping
   - Twitter: API v2 requires authentication
   - Solution: Simulated/mock data for demo, production requires credentials

2. **Data Freshness**
   - Web scraping may miss recent posts
   - RSS feeds have inherent delays
   - Solution: Run weekly to balance freshness vs. stability

3. **Relevance Scoring**
   - Keyword matching may include false positives
   - Solution: Manual review of top signals recommended

4. **Scale**
   - Top 1,000 companies may require multiple sources
   - Solution: Aggregates from multiple job boards

5. **Rate Limits**
   - Some APIs have strict limits
   - Solution: Distributed collection over time, caching

## Production Considerations

1. **Authentication**: Store API keys in environment variables or secrets manager
2. **Error Handling**: Retry logic for transient failures
3. **Logging**: Structured logging for monitoring and debugging
4. **Storage**: Consider database for historical tracking
5. **Alerting**: Notify on significant changes or errors
6. **Cost**: Monitor API usage and scraping costs

