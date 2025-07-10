"""
News fetching functionality for external APIs.
"""

import requests
import json
import os
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
from ..crud.server_crud import list_external_servers, update_server_status

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Handles fetching news from external APIs with smart rotation."""
    
    def __init__(self):
        # News API endpoints with smart rotation
        self.news_apis = [
            {
                'name': 'NewsAPI',
                'base_url': 'https://newsapi.org/v2/top-headlines',
                'params': {
                    'country': 'us',
                    'apiKey': os.getenv('NEWS_API_KEY', 'your-news-api-key')
                },
                'priority': 1,
                'daily_limit': 100,
                'requests_today': 0,
                'last_reset': datetime.now().date()
            },
            {
                'name': 'TheNewsAPI',
                'base_url': 'https://api.thenewsapi.com/v1/news/all',
                'params': {
                    'api_token': os.getenv('THENEWS_API_KEY', 'your-thenews-api-key'),
                    'language': 'en'
                },
                'priority': 2,
                'daily_limit': 50,
                'requests_today': 0,
                'last_reset': datetime.now().date()
            }
        ]
        
        self._initialize_api_status()
    
    def _initialize_api_status(self):
        """Initialize API status from database."""
        try:
            servers = list_external_servers()
            for server in servers:
                server_id, name, status, last_access, priority = server
                for api in self.news_apis:
                    if api['name'] in name:
                        api['status'] = status
                        api['last_access'] = last_access
                        api['priority'] = priority
                        break
        except Exception as e:
            logger.error(f"Error initializing API status: {e}")
    
    def _get_active_api(self) -> Optional[Dict[str, Any]]:
        """Get the currently active API based on priority and limits."""
        today = datetime.now().date()
        
        # Reset daily counters if it's a new day
        for api in self.news_apis:
            if api['last_reset'] != today:
                api['requests_today'] = 0
                api['last_reset'] = today
        
        # Sort APIs by priority (lower number = higher priority)
        sorted_apis = sorted(self.news_apis, key=lambda x: x['priority'])
        
        for api in sorted_apis:
            if (api.get('status', 'Active') == 'Active' and 
                api['requests_today'] < api['daily_limit']):
                return api
        
        # If no active APIs available, try to reactivate the first one
        if sorted_apis:
            logger.warning("No active APIs available, attempting to reactivate primary API")
            self._reactivate_api(sorted_apis[0])
            return sorted_apis[0]
        
        return None
    
    def _reactivate_api(self, api: Dict[str, Any]):
        """Reactivate an API by resetting its daily counter."""
        api['requests_today'] = 0
        api['status'] = 'Active'
        logger.info(f"Reactivated {api['name']}")
    
    def _update_api_status(self, api: Dict[str, Any], success: bool = True, error_message: str = None):
        """Update API status and request count."""
        api['requests_today'] += 1
        api['last_access'] = datetime.now().isoformat()
        
        if not success:
            api['status'] = 'Not Active'
            logger.error(f"API {api['name']} failed: {error_message}")
        else:
            api['status'] = 'Active'
            logger.info(f"API {api['name']} request successful (requests today: {api['requests_today']}/{api['daily_limit']})")
        
        self._update_database_api_status(api)
    
    def _update_database_api_status(self, api: Dict[str, Any]):
        """Update API status in database."""
        try:
            servers = list_external_servers()
            for server in servers:
                server_id, name, status, last_access, priority = server
                if api['name'] in name:
                    update_server_status(server_id, api['status'], api['last_access'])
                    break
        except Exception as e:
            logger.error(f"Error updating database API status: {e}")
    
    def fetch_news(self) -> List[Dict[str, Any]]:
        """Fetch news from external APIs with smart rotation."""
        logger.info("Starting news fetch...")
        
        active_api = self._get_active_api()
        if not active_api:
            logger.error("No active APIs available for news fetching")
            return []
        
        logger.info(f"Using {active_api['name']} (Priority: {active_api['priority']}, Requests: {active_api['requests_today']}/{active_api['daily_limit']})")
        
        try:
            articles = self._fetch_from_api(active_api)
            if articles:
                logger.info(f"Fetched {len(articles)} articles from {active_api['name']}")
                self._update_api_status(active_api, success=True)
                return articles
            else:
                self._update_api_status(active_api, success=False, error_message="No articles returned")
                return []
        except Exception as e:
            self._update_api_status(active_api, success=False, error_message=str(e))
            return self._try_next_api()
    
    def _try_next_api(self) -> List[Dict[str, Any]]:
        """Try the next available API if the current one fails."""
        logger.info("Trying next available API...")
        
        # Get the next available API
        active_api = self._get_active_api()
        if active_api:
            try:
                articles = self._fetch_from_api(active_api)
                if articles:
                    logger.info(f"Successfully fetched {len(articles)} articles from backup API {active_api['name']}")
                    self._update_api_status(active_api, success=True)
                    return articles
            except Exception as e:
                self._update_api_status(active_api, success=False, error_message=str(e))
        
        logger.error("All APIs failed")
        return []
    
    def _fetch_from_api(self, api_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch news from a specific API."""
        try:
            response = requests.get(api_config['base_url'], params=api_config['params'], timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if api_config['name'] == 'NewsAPI':
                return self._parse_newsapi_response(data)
            elif api_config['name'] == 'TheNewsAPI':
                return self._parse_thenewsapi_response(data)
            else:
                return self._parse_generic_response(data)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {api_config['name']}: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {api_config['name']}: {e}")
            raise
    
    def _parse_newsapi_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse NewsAPI response."""
        articles = []
        if 'articles' in data:
            for article in data['articles']:
                if article.get('title') and article.get('description'):
                    articles.append({
                        'title': article['title'],
                        'content': article['description'],
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'url': article.get('url', ''),
                        'category': None,  # NewsAPI doesn't provide categories
                        'keywords': [],
                        'published_date': article.get('publishedAt', datetime.now().isoformat())[:10]
                    })
        return articles
    
    def _parse_thenewsapi_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse TheNewsAPI response."""
        articles = []
        if 'data' in data:
            for article in data['data']:
                if article.get('title') and article.get('description'):
                    articles.append({
                        'title': article['title'],
                        'content': article['description'],
                        'source': article.get('source', 'Unknown'),
                        'url': article.get('url', ''),
                        'category': article.get('category', None),
                        'keywords': article.get('keywords', []),
                        'published_date': article.get('published_at', datetime.now().isoformat())[:10]
                    })
        return articles
    
    def _parse_generic_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse generic API response."""
        articles = []
        # This is a fallback for other APIs
        for item in data.get('articles', data.get('data', [])):
            if item.get('title') and item.get('description'):
                articles.append({
                    'title': item['title'],
                    'content': item['description'],
                    'source': item.get('source', 'Unknown'),
                    'url': item.get('url', ''),
                    'category': item.get('category', None),
                    'keywords': item.get('keywords', []),
                    'published_date': item.get('published_at', item.get('publishedAt', datetime.now().isoformat()))[:10]
                })
        return articles 