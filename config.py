"""
Configuration file for SaaS Security GTM Tracker
Contains search terms, keywords, and data source configurations
"""

# Hiring-related search terms
HIRING_KEYWORDS = {
    "saas_security": [
        "SaaS Security",
        "SaaS security engineer",
        "SaaS security analyst",
        "Cloud security engineer",
        "SaaS security architect"
    ],
    "sspm": [
        "SSPM",
        "SaaS Security Posture Management",
        "SaaS posture",
        "SaaS security posture"
    ],
    "ai_agent_security": [
        "AI agent security",
        "AI security engineer",
        "GenAI security",
        "AI agent defense",
        "AI security analyst"
    ],
    "saas_compliance": [
        "SaaS compliance",
        "SaaS compliance engineer",
        "SaaS governance",
        "Cloud compliance"
    ],
    "ai_compliance": [
        "AI compliance",
        "AI governance",
        "AI compliance engineer",
        "GenAI compliance"
    ]
}

# Conversation-related search terms
CONVERSATION_TOPICS = {
    "saas_security": [
        "SaaS Security",
        "SaaS security posture",
        "SaaS security management",
        "SaaS security platform"
    ],
    "sspm": [
        "SSPM",
        "SaaS Security Posture Management",
        "SaaS posture management"
    ],
    "saas_compliance": [
        "SaaS compliance",
        "SaaS governance",
        "SaaS regulatory compliance"
    ],
    "ai_agent_security": [
        "AI agent security",
        "AI agent defense",
        "GenAI security",
        "AI agent threat"
    ],
    "salesforce_breach": [
        "Salesforce breach",
        "Salesforce data breach",
        "Salesforce security incident"
    ],
    "gainsight_breach": [
        "Gainsight breach",
        "Gainsight data breach",
        "Gainsight security"
    ],
    "salesloft_breach": [
        "Salesloft breach",
        "Salesloft data breach",
        "Salesloft security incident"
    ]
}

# Top 10 Cybersecurity Publishers
CYBERSECURITY_PUBLISHERS = [
    {
        "name": "The Hacker News",
        "url": "https://thehackernews.com",
        "rss": "https://feeds.feedburner.com/TheHackersNews"
    },
    {
        "name": "Dark Reading",
        "url": "https://www.darkreading.com",
        "rss": "https://www.darkreading.com/rss.xml"
    },
    {
        "name": "SecurityWeek",
        "url": "https://www.securityweek.com",
        "rss": "https://www.securityweek.com/rss"
    },
    {
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com",
        "rss": "https://krebsonsecurity.com/feed/"
    },
    {
        "name": "Bleeping Computer",
        "url": "https://www.bleepingcomputer.com",
        "rss": "https://www.bleepingcomputer.com/feed/"
    },
    {
        "name": "Threatpost",
        "url": "https://threatpost.com",
        "rss": "https://threatpost.com/feed/"
    },
    {
        "name": "CSO Online",
        "url": "https://www.csoonline.com",
        "rss": "https://www.csoonline.com/index.rss"
    },
    {
        "name": "SC Magazine",
        "url": "https://www.scmagazine.com",
        "rss": "https://www.scmagazine.com/rss"
    },
    {
        "name": "InfoSecurity Magazine",
        "url": "https://www.infosecurity-magazine.com",
        "rss": "https://www.infosecurity-magazine.com/rss/news/"
    },
    {
        "name": "Security Boulevard",
        "url": "https://securityboulevard.com",
        "rss": "https://securityboulevard.com/feed/"
    }
]

# Job board configurations
JOB_BOARDS = {
    "indeed": {
        "base_url": "https://www.indeed.com/jobs",
        "max_results": 1000
    },
    "linkedin": {
        "base_url": "https://www.linkedin.com/jobs/search",
        "max_results": 1000
    }
}

# Social media configurations
SOCIAL_MEDIA = {
    "twitter": {
        "max_results": 100,
        "time_range": "7d"  # Last 7 days
    },
    "reddit": {
        "max_results": 100,
        "time_range": "week"
    }
}

# Output settings
OUTPUT_DIR = "outputs"
TOP_COMPANIES_LIMIT = 1000
TOP_PEOPLE_LIMIT = 500

