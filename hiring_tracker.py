"""
Hiring Signal Tracker
Identifies companies actively hiring for SaaS security-related roles
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
from fake_useragent import UserAgent
from config import HIRING_KEYWORDS, JOB_BOARDS, TOP_COMPANIES_LIMIT
import json

ua = UserAgent()

class HiringTracker:
    def __init__(self):
        self.companies = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': ua.random
        })
    
    def search_indeed(self, keyword, location="United States"):
        """Search Indeed for job postings"""
        companies = {}
        try:
            # Indeed search URL
            url = f"https://www.indeed.com/jobs"
            params = {
                'q': keyword,
                'l': location,
                'start': 0
            }
            
            # Note: In production, you'd want to paginate through results
            # For this prototype, we'll simulate with a limited search
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:50]:  # Limit for prototype
                    try:
                        company_elem = card.find('span', class_='companyName')
                        if company_elem:
                            company_name = company_elem.get_text(strip=True)
                            if company_name:
                                if company_name not in companies:
                                    companies[company_name] = {
                                        'count': 0,
                                        'roles': [],
                                        'keywords': []
                                    }
                                companies[company_name]['count'] += 1
                                companies[company_name]['keywords'].append(keyword)
                                
                                # Extract job title
                                title_elem = card.find('h2', class_='jobTitle')
                                if title_elem:
                                    job_title = title_elem.get_text(strip=True)
                                    companies[company_name]['roles'].append(job_title)
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"Error searching Indeed for {keyword}: {str(e)}")
        
        return companies
    
    def search_linkedin_simulated(self, keyword):
        """
        Simulated LinkedIn search
        Note: LinkedIn has strict anti-scraping measures.
        In production, you'd use:
        - LinkedIn API (requires partnership)
        - Selenium with proper rate limiting
        - Third-party services like Apify
        """
        companies = {}
        
        # Simulated data structure - in production, this would be actual scraping
        # For demonstration, we'll create a mock response
        print(f"[LinkedIn] Simulated search for: {keyword}")
        print("[LinkedIn] Note: Actual LinkedIn scraping requires careful implementation")
        
        # Example: You might use Selenium here
        # from selenium import webdriver
        # driver = webdriver.Chrome()
        # driver.get(f"https://www.linkedin.com/jobs/search/?keywords={keyword}")
        # ... scraping logic ...
        
        return companies
    
    def collect_hiring_signals(self):
        """Collect hiring signals from all sources"""
        print("Collecting hiring signals...")
        
        all_companies = {}
        
        # Search across all keyword categories
        for category, keywords in HIRING_KEYWORDS.items():
            print(f"Searching for {category} roles...")
            
            for keyword in keywords:
                # Search Indeed
                indeed_companies = self.search_indeed(keyword)
                for company, data in indeed_companies.items():
                    if company not in all_companies:
                        all_companies[company] = {
                            'company_name': company,
                            'total_jobs': 0,
                            'categories': set(),
                            'roles': [],
                            'sources': []
                        }
                    all_companies[company]['total_jobs'] += data['count']
                    all_companies[company]['categories'].add(category)
                    all_companies[company]['roles'].extend(data['roles'])
                    all_companies[company]['sources'].append('Indeed')
                
                # Add delay to respect rate limits
                time.sleep(2)
                
                # LinkedIn (simulated)
                linkedin_companies = self.search_linkedin_simulated(keyword)
                for company, data in linkedin_companies.items():
                    if company not in all_companies:
                        all_companies[company] = {
                            'company_name': company,
                            'total_jobs': 0,
                            'categories': set(),
                            'roles': [],
                            'sources': []
                        }
                    all_companies[company]['total_jobs'] += data['count']
                    all_companies[company]['categories'].add(category)
                    all_companies[company]['roles'].extend(data['roles'])
                    all_companies[company]['sources'].append('LinkedIn')
        
        # Convert sets to lists for JSON serialization
        for company in all_companies.values():
            company['categories'] = list(company['categories'])
            company['sources'] = list(set(company['sources']))
        
        return all_companies
    
    def rank_companies(self, companies):
        """Rank companies by hiring activity"""
        # Convert to list and sort by total_jobs
        company_list = list(companies.values())
        company_list.sort(key=lambda x: x['total_jobs'], reverse=True)
        
        # Add ranking
        for i, company in enumerate(company_list[:TOP_COMPANIES_LIMIT], 1):
            company['rank'] = i
            company['signal_strength'] = self._calculate_signal_strength(company)
        
        return company_list[:TOP_COMPANIES_LIMIT]
    
    def _calculate_signal_strength(self, company):
        """Calculate signal strength based on multiple factors"""
        score = 0
        
        # More jobs = stronger signal
        score += company['total_jobs'] * 10
        
        # More categories = broader hiring
        score += len(company['categories']) * 5
        
        # Multiple sources = more reliable
        score += len(company['sources']) * 3
        
        if score >= 100:
            return "Very High"
        elif score >= 50:
            return "High"
        elif score >= 20:
            return "Medium"
        else:
            return "Low"
    
    def generate_output(self, ranked_companies):
        """Generate CSV output"""
        df_data = []
        for company in ranked_companies:
            df_data.append({
                'Rank': company['rank'],
                'Company Name': company['company_name'],
                'Total Jobs': company['total_jobs'],
                'Categories': ', '.join(company['categories']),
                'Signal Strength': company['signal_strength'],
                'Sample Roles': '; '.join(company['roles'][:5]),  # First 5 roles
                'Data Sources': ', '.join(company['sources']),
                'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(df_data)
        return df

