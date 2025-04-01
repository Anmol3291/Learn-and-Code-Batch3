import requests
import json


class TumblrBlog:
    BASE_URL = "https://{blog_name}.tumblr.com/api/read/json"

    def __init__(self, blog_name):
        self.blog_name = blog_name

    def fetch_blog_data(self, start, number_of_posts):
        """Fetch blog data from Tumblr API."""
        try:
            url = self.BASE_URL.format(blog_name=self.blog_name)
            params = {"type": "photo", "num": number_of_posts, "start": start}
            response = requests.get(url, params=params)
            response_text = (
                response.text.replace("var tumblr_api_read = ", "").strip().rstrip(";")
            )
            return self.parse_json(response_text)
        except Exception as error:
            print(f"Error occurred while fetching data: {error}")
            return None

    @staticmethod
    def parse_json(json_text):
        """Parse JSON response."""
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as error:
            print(f"Error decoding JSON: {error}")
            return None

    def extract_blog_metadata(self, blog_data):
        """Extract metadata from the blog data."""
        return {
            "title": blog_data.get("tumblelog", {}).get("title"),
            "name": blog_data.get("tumblelog", {}).get("name"),
            "description": blog_data.get("tumblelog", {}).get("description"),
            "total_posts": blog_data.get("posts-total"),
        }

    def display_blog_metadata(self, metadata):
        """Display blog metadata."""
        print("\nTitle:", metadata["title"])
        print("Name:", metadata["name"])
        print("Description:", metadata["description"])
        print("Number of posts:", metadata["total_posts"])

    def display_blog_posts(self, posts, start_post, end_post):
        """Display blog posts within the given range."""
        for i in range(start_post, end_post):
            if i < len(posts):
                print(f"\nPost {i + 1}: {posts[i].get('photo-url-1280')}")

    def display_blog_info(self, blog_data, start_post, end_post):
        """Display complete blog information."""
        if not blog_data:
            print("No blog data available.")
            return

        metadata = self.extract_blog_metadata(blog_data)
        self.display_blog_metadata(metadata)

        posts = blog_data.get("posts", [])
        self.display_blog_posts(posts, start_post, end_post)


if __name__ == "__main__":
    blog_topic_name = input("Enter the topic name for Tumblr: \n")
    start_post = int(input("Enter the start post number: \n"))
    end_post = int(input("Enter the end post number: \n"))
    number_of_posts = end_post - start_post + 1

    tumblr_blog = TumblrBlog(blog_topic_name)
    blog_details = tumblr_blog.fetch_blog_data(
        start=start_post, number_of_posts=number_of_posts
    )

    tumblr_blog.display_blog_info(blog_details, start_post, end_post)
