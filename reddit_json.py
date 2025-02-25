import requests
import datetime 

def parse_reddit(reddit_key):
    # get Reddit API
    reddit_response = requests.get(reddit_key)
    
    # print the status code and response content
    print(f"Reddit API Status Code: {reddit_response.status_code}")
    print(f"Reddit API Response: {reddit_response.text}")
    
    # check if the request was successful
    if reddit_response.status_code != 200:
        print(f"Error: Status Code: {reddit_response.status_code}")
        return []
    # parse Reddit JSON
    reddit_response_json = reddit_response.json()
    # extract data
    data = reddit_response_json.get("data")
    children = data.get("children")
    
    reddit_posts = []
    for post in children:
        # parse each child
        post_data = post.get("data")
        if not post_data:
            continue  # skip if post data is missing
        
        # append titles, subreddits, upvotes, thumbnails, time, and URL
        reddit_posts.append({
            "title": post_data.get("title"),
            "subreddit": post_data.get("subreddit"),
            "upvotes": post_data.get("ups"),
            "thumbnail": post_data.get("thumbnail"),
            "time": convert_time(post_data.get("created")),
            "id": post_data.get("id"),
            "url": "https://redd.it/" + post_data.get("id"),
        })
    
    return reddit_posts

def convert_time(unix_time):
    # convert unix time to data time
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

# https://www.reddit.com/r/pics/comments/1ig887h/buy_canadian_instead_signs_going_up_in_bc_liquor/
# short link: https://redd.it/1ig887h