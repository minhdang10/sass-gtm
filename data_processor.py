"""
Data Processing Module
Handles data cleaning, deduplication, and enrichment
"""

import pandas as pd
import re
from datetime import datetime

class DataProcessor:
    def __init__(self):
        pass
    
    def clean_company_name(self, name):
        """Clean and normalize company names"""
        if not name:
            return ""
        
        # Remove common suffixes/prefixes
        name = re.sub(r'\s+Inc\.?$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+LLC\.?$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+Corp\.?$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+Ltd\.?$', '', name, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        return name.strip()
    
    def deduplicate_companies(self, companies):
        """Deduplicate companies with similar names"""
        # Group by normalized name
        normalized_map = {}
        
        for company in companies:
            normalized = self.clean_company_name(company['company_name']).lower()
            
            if normalized not in normalized_map:
                normalized_map[normalized] = company
            else:
                # Merge data
                existing = normalized_map[normalized]
                existing['total_jobs'] += company['total_jobs']
                existing['categories'] = list(set(existing['categories'] + company['categories']))
                existing['roles'].extend(company['roles'])
                existing['sources'] = list(set(existing['sources'] + company['sources']))
        
        return list(normalized_map.values())
    
    def enrich_company_data(self, company):
        """Add additional metadata to company records"""
        # Add company size estimate based on job count
        if company['total_jobs'] >= 20:
            company['estimated_size'] = 'Large'
        elif company['total_jobs'] >= 10:
            company['estimated_size'] = 'Medium'
        else:
            company['estimated_size'] = 'Small'
        
        # Add hiring intensity
        if company['total_jobs'] >= 15:
            company['hiring_intensity'] = 'Very Active'
        elif company['total_jobs'] >= 8:
            company['hiring_intensity'] = 'Active'
        elif company['total_jobs'] >= 3:
            company['hiring_intensity'] = 'Moderate'
        else:
            company['hiring_intensity'] = 'Low'
        
        return company
    
    def filter_relevant_roles(self, roles, keywords):
        """Filter roles to only include relevant ones"""
        relevant_roles = []
        keyword_lower = [k.lower() for k in keywords]
        
        for role in roles:
            role_lower = role.lower()
            if any(kw in role_lower for kw in keyword_lower):
                relevant_roles.append(role)
        
        return relevant_roles if relevant_roles else roles[:3]  # Return top 3 if no match

