import requests
import datetime 

def parse_reddit(reddit_key):
    # get json through reddit API
    reddit_response = requests.get(reddit_key)

    # parse reddit json
    reddit_response_json = reddit_response.json()
    reddit_response_json = reddit_response_json.get("data").get("children")
    reddit_posts = []

    for post in reddit_response_json:
        # parse each child json
        post = post["data"]
        # append titles, subreddits, upvotes, thumbnails, time, and url
        reddit_posts.append({
            "title": post["title"],
            "subreddit": post["subreddit"],
            "upvotes": post["ups"],
            "thumbnail": post["thumbnail"],
            "time": convert_time(post["created"]),
            "id": post["id"],
            "url": "https://redd.it/" + post["id"],
            })

    return reddit_posts

def convert_time(unix_time):
    # convert unix time to data time
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

# https://www.reddit.com/r/pics/comments/1ig887h/buy_canadian_instead_signs_going_up_in_bc_liquor/
# short link: https://redd.it/1ig887h