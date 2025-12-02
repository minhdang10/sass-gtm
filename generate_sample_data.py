"""
Sample Data Generator
Generates realistic sample data for demonstration purposes
This simulates what the system would produce with real data sources
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from config import OUTPUT_DIR, CONVERSATION_TOPICS
import os

# Sample company names (mix of real and representative)
SAMPLE_COMPANIES = [
    "Microsoft", "Google", "Amazon", "Salesforce", "Oracle", "IBM", "Cisco",
    "Palo Alto Networks", "CrowdStrike", "Zscaler", "Okta", "Auth0", "Splunk",
    "Datadog", "New Relic", "ServiceNow", "Workday", "Snowflake", "Databricks",
    "GitHub", "GitLab", "Atlassian", "Slack", "Zoom", "Dropbox", "Box",
    "DocuSign", "HubSpot", "Marketo", "Tableau", "Looker", "MongoDB",
    "Elastic", "Confluent", "Hashicorp", "Twilio", "Stripe", "Square",
    "Shopify", "SquareSpace", "Wix", "Squarespace", "Cloudflare", "Fastly",
    "Akamai", "F5 Networks", "Fortinet", "Check Point", "Proofpoint",
    "Mimecast", "Barracuda", "Trend Micro", "McAfee", "Symantec",
    "Rapid7", "Qualys", "Tenable", "RSA", "CyberArk", "SailPoint",
    "ForgeRock", "Ping Identity", "OneLogin", "Duo Security", "Twilio",
    "SendGrid", "Mailchimp", "Constant Contact", "Hootsuite", "Buffer",
    "Sprout Social", "Zendesk", "Freshdesk", "Intercom", "Drift",
    "Calendly", "Asana", "Monday.com", "Trello", "Notion", "Airtable",
    "Monday.com", "Smartsheet", "Monday.com", "Wrike", "ClickUp",
    "Basecamp", "Jira", "Confluence", "Bitbucket", "Jenkins", "CircleCI",
    "Travis CI", "GitLab CI", "GitHub Actions", "AWS", "Azure", "GCP",
    "DigitalOcean", "Linode", "Vultr", "Heroku", "Netlify", "Vercel"
]

# Sample job roles
SAMPLE_ROLES = [
    "SaaS Security Engineer", "Cloud Security Architect", "SaaS Security Analyst",
    "SSPM Engineer", "SaaS Compliance Manager", "AI Security Engineer",
    "GenAI Security Specialist", "SaaS Security Posture Manager",
    "Cloud Security Engineer", "SaaS Governance Analyst", "AI Compliance Engineer",
    "SaaS Security Consultant", "Security Engineer - SaaS", "SaaS Risk Analyst"
]

# Sample categories
CATEGORIES = [
    "saas_security", "sspm", "ai_agent_security", "saas_compliance", "ai_compliance"
]

# Sample usernames for social media
SAMPLE_USERNAMES = [
    "@securityexpert", "@cloudsecpro", "@saassec", "@cyberdefender",
    "@infosecpro", "@securityguru", "@cloudarchitect", "@secops",
    "@saascompliance", "@aisecurity", "@sspmexpert", "@cyberanalyst",
    "@securityresearcher", "@cloudsecurity", "@saassecops", "@infosec",
    "@securityengineer", "@cybersecurity", "@cloudops", "@devsecops"
]

# Sample post titles
SAMPLE_POSTS = [
    "New SaaS security framework released",
    "SSPM best practices for 2025",
    "AI agent security concerns in enterprise SaaS",
    "Salesforce breach analysis and lessons learned",
    "Gainsight incident: what we know so far",
    "Salesloft supply chain attack deep dive",
    "SaaS compliance requirements for healthcare",
    "AI compliance regulations update",
    "SaaS security posture management guide",
    "GenAI security risks in SaaS platforms"
]

def generate_hiring_signals():
    """Generate sample hiring signals"""
    companies = []
    
    # Generate top 1000 companies (using sample list with variations)
    for i in range(1000):
        base_company = random.choice(SAMPLE_COMPANIES)
        # Add some variation
        if random.random() < 0.3:
            company_name = f"{base_company} {random.choice(['Inc', 'LLC', 'Corp', 'Ltd', ''])}"
        else:
            company_name = base_company
        
        # Generate realistic job counts
        if i < 50:  # Top 50 have more jobs
            total_jobs = random.randint(15, 50)
        elif i < 200:  # Next 150
            total_jobs = random.randint(8, 20)
        elif i < 500:  # Next 300
            total_jobs = random.randint(3, 10)
        else:  # Rest
            total_jobs = random.randint(1, 5)
        
        # Select categories
        num_categories = random.randint(1, 3)
        selected_categories = random.sample(CATEGORIES, num_categories)
        
        # Generate roles
        num_roles = min(total_jobs, 10)
        roles = random.sample(SAMPLE_ROLES, min(num_roles, len(SAMPLE_ROLES)))
        
        # Calculate signal strength
        score = total_jobs * 10 + len(selected_categories) * 5 + 3
        if score >= 100:
            signal_strength = "Very High"
        elif score >= 50:
            signal_strength = "High"
        elif score >= 20:
            signal_strength = "Medium"
        else:
            signal_strength = "Low"
        
        companies.append({
            'Rank': i + 1,
            'Company Name': company_name,
            'Total Jobs': total_jobs,
            'Categories': ', '.join(selected_categories),
            'Signal Strength': signal_strength,
            'Sample Roles': '; '.join(roles[:5]),
            'Data Sources': random.choice(['Indeed', 'LinkedIn', 'Indeed, LinkedIn']),
            'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(companies)

def generate_conversation_signals_people():
    """Generate sample conversation signals for people"""
    people = []
    
    for i in range(500):
        username = random.choice(SAMPLE_USERNAMES)
        platform = random.choice(['X (Twitter)', 'Reddit'])
        
        # Generate engagement scores
        if i < 50:  # Top 50 influencers
            engagement = random.randint(1000, 5000)
        elif i < 200:
            engagement = random.randint(500, 1500)
        else:
            engagement = random.randint(50, 500)
        
        # Calculate influence score
        if engagement >= 1000:
            influence = "Very High"
        elif engagement >= 500:
            influence = "High"
        elif engagement >= 100:
            influence = "Medium"
        else:
            influence = "Low"
        
        # Select topics
        num_topics = random.randint(1, 4)
        topics = random.sample(list(CONVERSATION_TOPICS.keys()), min(num_topics, len(CONVERSATION_TOPICS)))
        
        num_posts = random.randint(1, 20)
        sample_post = random.choice(SAMPLE_POSTS)
        
        people.append({
            'Rank': i + 1,
            'Username/ID': username,
            'Platform': platform,
            'Engagement Score': engagement,
            'Influence Score': influence,
            'Topics Discussed': ', '.join(topics[:5]),
            'Number of Posts': num_posts,
            'Sample Post': sample_post,
            'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(people)

def generate_conversation_signals_publishers():
    """Generate sample conversation signals for publishers"""
    from config import CYBERSECURITY_PUBLISHERS
    
    publishers = []
    
    for i, pub in enumerate(CYBERSECURITY_PUBLISHERS):
        # Generate article counts
        if i < 3:  # Top 3 publishers
            num_articles = random.randint(15, 30)
        elif i < 7:
            num_articles = random.randint(8, 20)
        else:
            num_articles = random.randint(3, 12)
        
        # Select topics
        num_topics = random.randint(2, 5)
        topics = random.sample(list(CONVERSATION_TOPICS.keys()), min(num_topics, len(CONVERSATION_TOPICS)))
        
        sample_article = random.choice(SAMPLE_POSTS)
        
        publishers.append({
            'Rank': i + 1,
            'Publisher Name': pub['name'],
            'Relevance Score': num_articles,
            'Number of Articles': num_articles,
            'Topics Covered': ', '.join(topics[:5]),
            'Website URL': pub['url'],
            'Sample Article': sample_article,
            'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(publishers)

def main():
    """Generate all sample data files"""
    print("Generating sample data files...")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Generate hiring signals
    print("Generating hiring signals...")
    hiring_df = generate_hiring_signals()
    hiring_path = os.path.join(OUTPUT_DIR, "hiring_signals.csv")
    hiring_df.to_csv(hiring_path, index=False)
    print(f"✓ Generated {len(hiring_df)} company records")
    
    # Generate conversation signals - people
    print("Generating conversation signals (people)...")
    people_df = generate_conversation_signals_people()
    people_path = os.path.join(OUTPUT_DIR, "conversation_signals_people.csv")
    people_df.to_csv(people_path, index=False)
    print(f"✓ Generated {len(people_df)} people records")
    
    # Generate conversation signals - publishers
    print("Generating conversation signals (publishers)...")
    publishers_df = generate_conversation_signals_publishers()
    publishers_path = os.path.join(OUTPUT_DIR, "conversation_signals_publishers.csv")
    publishers_df.to_csv(publishers_path, index=False)
    print(f"✓ Generated {len(publishers_df)} publisher records")
    
    print("\nSample data generation complete!")
    print(f"\nOutput files:")
    print(f"  - {hiring_path}")
    print(f"  - {people_path}")
    print(f"  - {publishers_path}")

if __name__ == "__main__":
    main()

