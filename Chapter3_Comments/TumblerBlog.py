class TumblerBlog:
    """Represents a blog with its details."""

    def __init__(self, data):
        self.title = data.get("tumblelog", {}).get("title", "N/A")
        self.name = data.get("tumblelog", {}).get("name", "N/A")
        self.description = data.get("tumblelog", {}).get("description", "N/A")
        self.total_posts = data.get("posts-total", "N/A")
        self.posts = data.get("posts", [])

    def display_info(self):
        """Displays blog details."""
        print("\nTitle:", self.title)
        print("Name:", self.name)
        print("Description:", self.description)
        print("No of posts:", self.total_posts)

    def display_images(self, start_post, end_post):
        """Displays blog images."""
        for i in range(start_post, min(end_post, len(self.posts))):
            print(
                f"{i + 1}.", self.posts[i].get("photo-url-1280", "No Image Available")
            )
