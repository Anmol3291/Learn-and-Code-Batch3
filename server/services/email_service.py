"""
Email service for sending notifications and user communications.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email notifications and communications."""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@newsaggregator.com')
        
        self.email_enabled = bool(self.smtp_username and self.smtp_password)
        
        if not self.email_enabled:
            logger.warning("Email service not configured. Set SMTP_USERNAME and SMTP_PASSWORD environment variables.")
    
    def send_consolidated_notification(self, to_email: str, articles: List[dict]) -> bool:
        """Send consolidated notification with multiple articles."""
        if not articles:
            return False
            
        total_articles = len(articles)
        subject = f"News Aggregator - {total_articles} New Articles for You"
        
        # Group articles by category
        articles_by_category = {}
        for article in articles:
            category = article.get('category', 'General')
            if category not in articles_by_category:
                articles_by_category[category] = []
            articles_by_category[category].append(article)
        
        # Build HTML content
        content = f"""
        <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">📰 News Aggregator</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Your personalized news digest</p>
            </div>
            
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 25px; border-left: 4px solid #2196f3;">
                    <h2 style="margin: 0 0 10px 0; color: #1976d2; font-size: 20px;">🎯 {total_articles} New Articles Found!</h2>
                    <p style="margin: 0; color: #424242;">We've found {total_articles} articles that match your preferences. Here's your personalized news digest:</p>
                </div>
        """
        
        # Add articles grouped by category
        for category, category_articles in articles_by_category.items():
            content += f"""
                <div style="margin-bottom: 30px;">
                    <h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-bottom: 20px;">
                        📂 {category} ({len(category_articles)} articles)
                    </h3>
            """
            
            for article in category_articles:
                image_html = f'<img src="{article.get("image_url", "")}" alt="Article Image" style="max-width:100%;border-radius:6px;margin-bottom:10px;">' if article.get('image_url') else ''
                content += f"""
                    <div style="background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        {image_html}
                        <h4 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;">
                            <a href="{article.get('url', '#')}" style="color: #3498db; text-decoration: none; font-weight: bold;">
                                {article.get('title', 'No title')}
                            </a>
                        </h4>
                        <p style="margin: 0 0 15px 0; color: #666; line-height: 1.5; font-size: 14px;">
                            {article.get('content', '')[:150]}...
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #888;">
                            <span>📰 {article.get('source', 'Unknown')}</span>
                            <span>📅 {article.get('published_date', 'Unknown date')}</span>
                        </div>
                        <div style="margin-top: 15px;">
                            <a href="{article.get('url', '#')}" style="background-color: #3498db; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px; font-size: 14px; display: inline-block;">
                                📖 Read Full Article
                            </a>
                        </div>
                    </div>
                """
            
            content += "</div>"
        
        # Add footer
        content += f"""
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin-top: 25px; text-align: center;">
                    <h3 style="margin: 0 0 15px 0; color: #2c3e50;">📊 Summary</h3>
                    <div style="display: flex; justify-content: space-around; text-align: center;">
                        <div>
                            <div style="font-size: 24px; font-weight: bold; color: #3498db;">{total_articles}</div>
                            <div style="font-size: 12px; color: #666;">Total Articles</div>
                        </div>
                        <div>
                            <div style="font-size: 24px; font-weight: bold; color: #27ae60;">{len(articles_by_category)}</div>
                            <div style="font-size: 12px; color: #666;">Categories</div>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <a href="http://localhost:3000" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        🏠 Visit News Aggregator
                    </a>
                </div>
                
                <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #666; font-size: 12px;">
                    <p style="margin: 0 0 5px 0;">This email was sent by News Aggregator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p style="margin: 0;">You can manage your notification preferences in your account settings.</p>
                </div>
            </div>
        </div>
        """
        
        return self.send_html_email(to_email, subject, content)
    
    def send_html_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send HTML formatted email directly."""
        try:
            message = MIMEMultipart('alternative')
            message['From'] = self.from_email
            message['To'] = to_email
            message['Subject'] = subject

            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"HTML email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send HTML email to {to_email}: {e}")
            return False
    
    def _create_email_template(self, content: str) -> str:
        """Create HTML email template with consistent styling."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News Aggregator Notification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 0 0 5px 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 12px;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .button {{
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
                .button:hover {{
                    background-color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>News Aggregator</h1>
            </div>
            <div class="content">
                {content}
            </div>
            <div class="footer">
                <p>This email was sent by News Aggregator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>You can manage your notification preferences in your account settings.</p>
            </div>
        </body>
        </html>
        """ 