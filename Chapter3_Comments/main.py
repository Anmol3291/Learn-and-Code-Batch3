from api_client import APIClient
from TumblrAPI import TumblrAPI
from TumblerBlog import TumblerBlog

if __name__ == "__main__":
    blog_topic_name = input("Enter the topic name for Tumblr: ")
    start_post = int(input("Enter the start post number: "))
    end_post = int(input("Enter the end post number: "))
    number_of_posts = end_post - start_post + 1

    api_client = APIClient()
    tumblr_api = TumblrAPI(blog_topic_name, api_client)
    blog_data = tumblr_api.fetch_blog_details(
        start=start_post, number_of_posts=number_of_posts
    )

    if blog_data:
        blog = TumblerBlog(blog_data)
        blog.display_info()
        blog.display_images(start_post, end_post)
    else:
        print("Failed to retrieve blog data.")
