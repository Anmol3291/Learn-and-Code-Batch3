"""
Sample data insertion for development and testing purposes.
"""

import json
import uuid
from datetime import datetime, timedelta
from .connection import get_db_connection


def insert_sample_articles():
    """Insert sample articles for development and testing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sample_articles = _get_sample_articles()
    
    for article in sample_articles:
        cursor.execute("""
            INSERT OR IGNORE INTO articles (id, title, content, source, url, category, keywords, published_date, created_at, likes, dislikes, vector_id, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, article)
    
    conn.commit()
    conn.close()
    print("Sample articles inserted successfully")


def _get_sample_articles():
    """Get list of sample articles with realistic data."""
    return [
        # Today's articles
        (
            str(uuid.uuid4()),
            "Tesla Unusual Options Activity - Tesla (NASDAQ: TSLA)",
            "Deep-pocketed investors have adopted a bearish approach towards Tesla TSLA, and it's something market players shouldn't ignore. Our tracking of public options reveals significant activity...",
            "benzinga.com",
            "https://www.benzinga.com/insights/options/25/03/44379781/tesla-unusual-options-activity",
            "Business",
            json.dumps(["Tesla", "TSLA", "options", "investors", "market"]),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            45, 12, None,
            "https://example.com/tesla.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Apple Announces New AI Features",
            "Apple Inc. has unveiled groundbreaking artificial intelligence features that will be integrated across its ecosystem. The new AI capabilities promise to revolutionize user experience...",
            "techcrunch.com",
            "https://www.techcrunch.com/2025/03/22/apple-ai-features",
            "Technology",
            json.dumps(["Apple", "AI", "artificial intelligence", "ecosystem", "features"]),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            123, 8, None,
            "https://example.com/apple.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Netflix Original Series Breaks Records",
            "The latest Netflix original series has shattered viewership records, becoming the most-watched show in the platform's history. The series garnered millions of viewers within its first week...",
            "variety.com",
            "https://www.variety.com/2025/03/22/netflix-record-breaking-series",
            "Entertainment",
            json.dumps(["Netflix", "series", "records", "viewership", "streaming"]),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            78, 15, None,
            "https://example.com/netflix.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Champions League Quarter-Finals Draw",
            "The UEFA Champions League quarter-finals draw has been completed, setting up exciting matchups between Europe's elite clubs. Football fans worldwide are eagerly anticipating these clashes...",
            "espn.com",
            "https://www.espn.com/soccer/2025/03/22/champions-league-draw",
            "Sports",
            json.dumps(["Champions League", "UEFA", "football", "soccer", "quarter-finals"]),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            92, 6, None,
            "https://example.com/champions-league.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Microsoft Cloud Revenue Surges",
            "Microsoft Corporation reported exceptional growth in its cloud computing division, with Azure revenue increasing by 35% year-over-year. The company's focus on AI-powered cloud services...",
            "reuters.com",
            "https://www.reuters.com/technology/2025/03/22/microsoft-cloud-revenue",
            "Business",
            json.dumps(["Microsoft", "Azure", "cloud", "revenue", "AI"]),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            67, 9, None,
            "https://example.com/microsoft-cloud.jpg",
        ),
        # Yesterday's articles
        (
            str(uuid.uuid4()),
            "Google Unveils Quantum Computing Breakthrough",
            "Google has announced a major breakthrough in quantum computing, claiming to have achieved quantum supremacy with their latest processor. This development could revolutionize computing...",
            "wired.com",
            "https://www.wired.com/2025/03/21/google-quantum-breakthrough",
            "Technology",
            json.dumps(["Google", "quantum computing", "breakthrough", "supremacy", "processor"]),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            156, 23, None,
            "https://example.com/google-quantum.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Hollywood Strikes Deal with AI Companies",
            "Major Hollywood studios have reached a landmark agreement with artificial intelligence companies regarding the use of AI in film production. The deal addresses concerns about job displacement...",
            "hollywoodreporter.com",
            "https://www.hollywoodreporter.com/2025/03/21/hollywood-ai-deal",
            "Entertainment",
            json.dumps(["Hollywood", "AI", "film production", "studios", "agreement"]),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            89, 34, None,
            "https://example.com/hollywood-ai.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Olympic Swimming Records Broken",
            "Multiple world records were shattered at the World Swimming Championships, with athletes delivering extraordinary performances. The competition showcased the incredible talent...",
            "swimnews.com",
            "https://www.swimnews.com/2025/03/21/world-records-broken",
            "Sports",
            json.dumps(["Olympic", "swimming", "records", "championships", "athletes"]),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            112, 5, None,
            "https://example.com/olympic-swimming.jpg",
        ),
        # Day before yesterday's articles
        (
            str(uuid.uuid4()),
            "Amazon Expands Drone Delivery Service",
            "Amazon has announced the expansion of its drone delivery service to 50 new cities across the United States. The company claims the service will significantly reduce delivery times...",
            "cnbc.com",
            "https://www.cnbc.com/2025/03/20/amazon-drone-delivery-expansion",
            "Business",
            json.dumps(["Amazon", "drone delivery", "expansion", "cities", "delivery times"]),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            134, 18, None,
            "https://example.com/amazon-drone-delivery.jpg",
        ),
        (
            str(uuid.uuid4()),
            "Virtual Reality Gaming Revolution",
            "The gaming industry is experiencing a virtual reality revolution with new immersive technologies that promise to change how we play games. Major gaming companies are investing heavily...",
            "gamespot.com",
            "https://www.gamespot.com/2025/03/20/vr-gaming-revolution",
            "Technology",
            json.dumps(["VR", "virtual reality", "gaming", "revolution", "immersive"]),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            datetime.now().isoformat(),
            201, 12, None,
            "https://example.com/vr-gaming.jpg",
        ),
    ] 