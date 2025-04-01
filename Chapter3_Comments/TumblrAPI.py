from config import Config
from api_client import APIClient


class TumblrAPI:
    """Fetches blog details from Tumblr."""

    def __init__(self, blog_name, api_client: APIClient):
        self.blog_name = blog_name
        self.api_client = api_client
        self.base_url = Config.BASE_URL.format(blog_name=blog_name)

    def fetch_blog_details(self, start, number_of_posts):
        url = f"{self.base_url}?type=photo&num={number_of_posts}&start={start}"
        return self.api_client.fetch_data(url)
