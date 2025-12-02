"""
Conversation Signal Tracker
Identifies people and publishers discussing SaaS security topics
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import time
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from config import CONVERSATION_TOPICS, CYBERSECURITY_PUBLISHERS, TOP_PEOPLE_LIMIT
import praw
import json

ua = UserAgent()

class ConversationTracker:
    def __init__(self):
        self.people = {}
        self.publishers = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': ua.random
        })
        
        # Initialize Reddit API (requires credentials in production)
        # For demo, we'll use a placeholder
        self.reddit = None
        try:
            # In production, set these as environment variables
            # self.reddit = praw.Reddit(
            #     client_id="your_client_id",
            #     client_secret="your_client_secret",
            #     user_agent="SaaS Security Tracker"
            # )
            pass
        except:
            pass
    
    def search_twitter_simulated(self, keyword):
        """
        Simulated Twitter/X search
        Note: Twitter API v2 requires authentication
        In production, use tweepy with API credentials
        """
        people = {}
        
        print(f"[Twitter] Simulated search for: {keyword}")
        print("[Twitter] Note: Actual Twitter search requires API credentials")
        
        # Example with tweepy (commented out - requires API keys):
        # import tweepy
        # client = tweepy.Client(bearer_token="your_token")
        # tweets = client.search_recent_tweets(
        #     query=keyword,
        #     max_results=100,
        #     tweet_fields=['author_id', 'created_at']
        # )
        # for tweet in tweets.data:
        #     author_id = tweet.author_id
        #     # Get user info and track
        
        return people
    
    def search_reddit(self, keyword, subreddits=None):
        """Search Reddit for discussions"""
        people = {}
        
        if subreddits is None:
            subreddits = ['cybersecurity', 'netsec', 'sysadmin', 'security', 'SaaS']
        
        if self.reddit is None:
            print(f"[Reddit] Simulated search for: {keyword}")
            print("[Reddit] Note: Actual Reddit search requires PRAW credentials")
            return people
        
        try:
            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    posts = subreddit.search(keyword, limit=25, time_filter='week')
                    
                    for post in posts:
                        author = str(post.author)
                        if author and author != 'None':
                            if author not in people:
                                people[author] = {
                                    'username': author,
                                    'platform': 'Reddit',
                                    'posts': [],
                                    'topics': set(),
                                    'engagement': 0
                                }
                            people[author]['posts'].append({
                                'title': post.title,
                                'score': post.score,
                                'url': post.url,
                                'created': datetime.fromtimestamp(post.created_utc).isoformat()
                            })
                            people[author]['topics'].add(keyword)
                            people[author]['engagement'] += post.score
                except Exception as e:
                    print(f"Error searching subreddit {subreddit_name}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error in Reddit search: {str(e)}")
        
        return people
    
    def search_publishers(self, keyword):
        """Search top cybersecurity publishers via RSS feeds"""
        publisher_data = {}
        
        for publisher in CYBERSECURITY_PUBLISHERS:
            try:
                print(f"Searching {publisher['name']} for: {keyword}")
                
                # Parse RSS feed
                feed = feedparser.parse(publisher['rss'])
                
                for entry in feed.entries[:20]:  # Limit per publisher
                    # Check if keyword appears in title or summary
                    title = entry.get('title', '').lower()
                    summary = entry.get('summary', '').lower()
                    keyword_lower = keyword.lower()
                    
                    if keyword_lower in title or keyword_lower in summary:
                        publisher_name = publisher['name']
                        
                        if publisher_name not in publisher_data:
                            publisher_data[publisher_name] = {
                                'publisher': publisher_name,
                                'articles': [],
                                'topics': set(),
                                'url': publisher['url']
                            }
                        
                        publisher_data[publisher_name]['articles'].append({
                            'title': entry.get('title', ''),
                            'link': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'summary': entry.get('summary', '')[:200]  # First 200 chars
                        })
                        publisher_data[publisher_name]['topics'].add(keyword)
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error searching {publisher['name']}: {str(e)}")
                continue
        
        return publisher_data
    
    def collect_conversation_signals(self):
        """Collect conversation signals from all sources"""
        print("Collecting conversation signals...")
        
        all_people = {}
        all_publishers = {}
        
        # Search across all topics
        for topic, keywords in CONVERSATION_TOPICS.items():
            print(f"Searching for discussions about: {topic}")
            
            for keyword in keywords:
                # Twitter/X
                twitter_people = self.search_twitter_simulated(keyword)
                for username, data in twitter_people.items():
                    if username not in all_people:
                        all_people[username] = data
                    else:
                        all_people[username]['posts'].extend(data['posts'])
                        all_people[username]['topics'].update(data['topics'])
                        all_people[username]['engagement'] += data['engagement']
                
                # Reddit
                reddit_people = self.search_reddit(keyword)
                for username, data in reddit_people.items():
                    if username not in all_people:
                        all_people[username] = data
                    else:
                        all_people[username]['posts'].extend(data['posts'])
                        all_people[username]['topics'].update(data['topics'])
                        all_people[username]['engagement'] += data['engagement']
                
                # Publishers
                publisher_results = self.search_publishers(keyword)
                for pub_name, pub_data in publisher_results.items():
                    if pub_name not in all_publishers:
                        all_publishers[pub_name] = pub_data
                    else:
                        all_publishers[pub_name]['articles'].extend(pub_data['articles'])
                        all_publishers[pub_name]['topics'].update(pub_data['topics'])
                
                time.sleep(1)  # Rate limiting
        
        # Convert sets to lists
        for person in all_people.values():
            person['topics'] = list(person['topics'])
        
        for publisher in all_publishers.values():
            publisher['topics'] = list(publisher['topics'])
        
        return all_people, all_publishers
    
    def rank_people(self, people):
        """Rank people by engagement and relevance"""
        people_list = list(people.values())
        
        # Sort by engagement (score, upvotes, etc.)
        people_list.sort(key=lambda x: x['engagement'], reverse=True)
        
        # Add ranking
        for i, person in enumerate(people_list[:TOP_PEOPLE_LIMIT], 1):
            person['rank'] = i
            person['influence_score'] = self._calculate_influence_score(person)
        
        return people_list[:TOP_PEOPLE_LIMIT]
    
    def rank_publishers(self, publishers):
        """Rank publishers by article count and relevance"""
        publisher_list = list(publishers.values())
        
        # Sort by number of relevant articles
        publisher_list.sort(key=lambda x: len(x['articles']), reverse=True)
        
        # Add ranking
        for i, publisher in enumerate(publisher_list, 1):
            publisher['rank'] = i
            publisher['relevance_score'] = len(publisher['articles'])
        
        return publisher_list
    
    def _calculate_influence_score(self, person):
        """Calculate influence score based on engagement"""
        score = person['engagement']
        
        if score >= 1000:
            return "Very High"
        elif score >= 500:
            return "High"
        elif score >= 100:
            return "Medium"
        else:
            return "Low"
    
    def generate_people_output(self, ranked_people):
        """Generate CSV output for people"""
        df_data = []
        for person in ranked_people:
            df_data.append({
                'Rank': person['rank'],
                'Username/ID': person['username'],
                'Platform': person['platform'],
                'Engagement Score': person['engagement'],
                'Influence Score': person['influence_score'],
                'Topics Discussed': ', '.join(person['topics'][:5]),
                'Number of Posts': len(person['posts']),
                'Sample Post': person['posts'][0]['title'] if person['posts'] else '',
                'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(df_data)
        return df
    
    def generate_publishers_output(self, ranked_publishers):
        """Generate CSV output for publishers"""
        df_data = []
        for publisher in ranked_publishers:
            df_data.append({
                'Rank': publisher['rank'],
                'Publisher Name': publisher['publisher'],
                'Relevance Score': publisher['relevance_score'],
                'Number of Articles': len(publisher['articles']),
                'Topics Covered': ', '.join(publisher['topics'][:5]),
                'Website URL': publisher['url'],
                'Sample Article': publisher['articles'][0]['title'] if publisher['articles'] else '',
                'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(df_data)
        return df

