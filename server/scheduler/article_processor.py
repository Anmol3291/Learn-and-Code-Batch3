"""
Article processing functionality for handling fetched news articles.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
import time
import sqlite3
from openai import OpenAI
from ..crud.article_crud import check_article_exists, add_article
from ..crud.category_crud import get_categories, add_category
from ..crud.vector_crud import save_article_vector
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class ArticleProcessor:
    """Handles processing and storing fetched news articles."""
    
    def __init__(self):
        self.processed_count = 0
        self.skipped_count = 0
        self.openai_client = None
        
        # Initialize OpenAI client if API key is available
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
    
    def process_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, int]:
        """Process a list of articles and store them in the database."""
        logger.info(f"Processing {len(articles)} articles...")
        
        self.processed_count = 0
        self.skipped_count = 0
        
        for article in articles:
            try:
                if self._process_single_article(article):
                    self.processed_count += 1
                else:
                    self.skipped_count += 1
                # Add small delay to prevent database locking
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing article '{article.get('title', 'Unknown')}': {e}")
                self.skipped_count += 1
        
        result = {
            'processed': self.processed_count,
            'skipped': self.skipped_count,
            'total': len(articles)
        }
        
        logger.info(f"Article processing complete: {result}")
        return result
    
    def _process_single_article(self, article: Dict[str, Any]) -> bool:
        """Process a single article and store it in the database."""
        # Validate required fields
        if not self._validate_article(article):
            return False
        
        # Check if article already exists
        if check_article_exists(article['url']):
            logger.info(f"📰 DUPLICATE SKIPPED: {article['title']}")
            return False
        
        # If no category is provided, suggest one using AI
        if not article.get('category'):
            suggested_category = self._suggest_category(article['title'], article['content'])
            article['category'] = suggested_category
            logger.info(f"🤖 AI CATEGORY SUGGESTED: '{suggested_category}' for '{article['title']}'")
        
        # If no keywords are provided, generate them using AI
        if not article.get('keywords'):
            suggested_keywords = self._suggest_keywords(article['title'], article['content'])
            article['keywords'] = suggested_keywords
            logger.info(f"🏷️ AI KEYWORDS GENERATED: {suggested_keywords} for '{article['title']}'")
        
        # Store article in database with retry logic
        article_id = self._save_article_with_retry(article)
        
        if article_id:
            # Enhanced logging with title and category
            category_display = article['category'] or 'Uncategorized'
            logger.info(f"✅ SAVED: [{category_display}] {article['title']}")
            
            # Create vector embedding for search
            self._create_article_vector(article_id, article)
            
            return True
        else:
            logger.error(f"Failed to store article: {article['title']}")
            return False
    
    def _save_article_with_retry(self, article_data: Dict[str, Any], max_retries: int = 3) -> Optional[int]:
        """Save article with retry logic for database locks."""
        for attempt in range(max_retries):
            try:
                return add_article(
                    title=article_data['title'],
                    content=article_data['content'],
                    source=article_data['source'],
                    url=article_data['url'],
                    category=article_data.get('category'),
                    keywords=article_data.get('keywords', []),
                    published_date=article_data.get('published_date')
                )
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Database locked, retrying in 1 second... (attempt {attempt + 1})")
                    time.sleep(1)
                    continue
                else:
                    raise e
            except Exception as e:
                raise e
        return None
    
    def _validate_article(self, article: Dict[str, Any]) -> bool:
        """Validate that article has required fields."""
        required_fields = ['title', 'content', 'source', 'url']
        
        for field in required_fields:
            if not article.get(field):
                logger.debug(f"Article missing required field: {field}")
                return False
        
        # Check minimum content length
        if len(article['content'].strip()) < 50:
            logger.debug(f"Article content too short: {article['title']}")
            return False
        
        return True
    
    def _suggest_category(self, title: str, content: str) -> str:
        """Suggest category using OpenAI."""
        if not self.openai_client:
            return "General"
        
        try:
            # get_categories returns a list of (id, name, created_at) tuples
            existing_categories_tuples = get_categories()
            existing_categories = [cat[1] for cat in existing_categories_tuples]
            
            prompt = f"""
            Given the following news article, suggest the most appropriate category from the existing categories or suggest a new one (maximum 3 new categories if needed).
            
            Article Title: {title}
            Article Content: {content[:500]}...
            
            Existing Categories: {', '.join(existing_categories)}
            
            Please respond with only the category name. If none of the existing categories fit well, suggest up to 3 new categories separated by commas.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.3
            )
            
            if response and response.choices and response.choices[0]:
                suggested = response.choices[0].message.content.strip()
                
                # If it's an existing category, return it
                if suggested in existing_categories:
                    return suggested
                
                # If it's a new category, add it to the database
                if suggested and ',' not in suggested:
                    if add_category(suggested):
                        return suggested
                
                return "General"
            else:
                return "General"
            
        except Exception as e:
            logger.error(f"Error suggesting category: {e}")
            return "General"
    
    def _suggest_keywords(self, title: str, content: str) -> List[str]:
        """Suggest keywords using OpenAI."""
        if not self.openai_client:
            return []
        
        try:
            prompt = f"""
            Extract 5-8 relevant keywords from this news article. Return only the keywords separated by commas.
            
            Article Title: {title}
            Article Content: {content[:300]}...
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            
            if response and response.choices and response.choices[0]:
                keywords_text = response.choices[0].message.content.strip()
                keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
                
                return keywords[:8]  # Limit to 8 keywords
            else:
                return []
            
        except Exception as e:
            logger.error(f"Error suggesting keywords: {e}")
            return []
    
    def _create_article_vector(self, article_id: int, article_data: Dict[str, Any]):
        """Create vector embedding for article search."""
        try:
            # For now, we'll create a simple text representation
            # In a full implementation, you'd use a proper embedding model
            text_for_vector = f"{article_data['title']} {article_data['content'][:500]}"
            
            # Simple vector representation (in production, use proper embeddings)
            vector_data = {
                'text': text_for_vector,
                'title': article_data['title'],
                'category': article_data.get('category'),
                'keywords': article_data.get('keywords', [])
            }
            
            save_article_vector(article_id, vector_data)
            
        except Exception as e:
            logger.error(f"Error creating article vector: {e}")
    
    def get_processing_stats(self) -> Dict[str, int]:
        """Get current processing statistics."""
        return {
            'processed': self.processed_count,
            'skipped': self.skipped_count,
            'total': self.processed_count + self.skipped_count
        }
    
    def reset_stats(self):
        """Reset processing statistics."""
        self.processed_count = 0
        self.skipped_count = 0 