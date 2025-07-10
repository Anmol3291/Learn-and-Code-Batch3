"""
CRUD operations module - imports all database operation modules.
"""

# Import database connection
from ..database.connection import get_db_connection

# Import all CRUD modules for easy access
from .user_crud import (
    get_user, get_user_by_username, create_user, get_user_by_id,
    update_user_role, delete_user
)

from .server_crud import (
    list_external_servers, get_server_details, update_server_api,
    update_server_status, get_api_info, reset_api_daily_counters
)

from .category_crud import (
    add_category, get_categories, get_category_by_name,
    delete_category, update_category
)

from .article_crud import (
    get_articles_by_date, get_articles_by_date_range,
    get_articles_by_date_and_category, get_articles_by_date_range_and_category,
    check_article_exists, add_article, get_articles_count,
    get_articles_count_by_range, get_article_by_id,
    delete_article, update_article
)

from .saved_article_crud import (
    save_article, get_saved_articles, delete_saved_article,
    get_saved_articles_count, is_article_saved
)

from .reaction_crud import (
    like_article, dislike_article, unlike_article, remove_dislike,
    get_liked_articles, get_disliked_articles,
    get_liked_articles_count, get_disliked_articles_count,
    get_article_reaction_stats, get_user_reaction
)

from .search_crud import (
    search_articles, search_articles_count, search_by_keywords,
    search_by_keywords_count, get_popular_articles, get_recent_articles
)

from .notification_crud import (
    get_user_notifications, get_user_notification_config,
    update_user_notification_config, get_user_keywords,
    update_user_keywords, create_notification,
    mark_notification_email_sent, delete_notification,
    delete_user_notifications, get_users_for_category_notification,
    get_users_for_keyword_notification
)

from .vector_crud import (
    save_article_vector, get_article_vector, delete_article_vector,
    get_all_vectors, update_article_vector_id
) 