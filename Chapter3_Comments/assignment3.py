import requests
import json


def get_blog_detials(blog_topic_name, start, number_of_posts):
    try:
        url = f"https://{blog_topic_name}.tumblr.com/api/read/json?type=photo&num={number_of_posts}&start={start}"
        response = requests.get(url)
        json_response = (
            response.text.replace("var tumblr_api_read = ", "").strip().replace(";", "")
        )
        return json.loads(json_response)
    except Exception as error:
        print(f"Error Occured while fetching data : {error}")


def display_blog_related_information(blog_data, start_post, end_post):
    blog_title = blog_data.get("tumblelog").get("title")
    blog_name = blog_data.get("tumblelog").get("name")
    blog_description = blog_data.get("tumblelog").get("description")
    total_posts = blog_data.get("posts-total")
    posts = blog_data.get("posts")

    print("\ntitle:", blog_title)
    print("name:", blog_name)
    print("description:", blog_description)
    print("no of post:", total_posts)

    for i in range(start_post, end_post):
        print(f"{i}.", posts[i].get("photo-url-1280"))


if __name__ == "__main__":
    blog_topic_name = input("Enter the topic name for Tumblr: \n")
    start_post = int(input("Enter the start post number: \n"))
    end_post = int(input("Enter the end post number: \n"))
    number_of_posts = end_post - start_post + 1

    blog_details = get_blog_detials(
        blog_topic_name=blog_topic_name,
        start=start_post,
        number_of_posts=number_of_posts,
    )

    display_blog_related_information(blog_details, start_post, end_post)
