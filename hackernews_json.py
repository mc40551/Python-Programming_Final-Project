import requests
import datetime 

def parse_hackernews(hackernews_key):
    # access API
    news_response = requests.get(hackernews_key).json()[:10]
    articles = []
    for article in news_response:
        # since the json file only contains article IDs, we need to retrieve information of each ID
        article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{article}.json").json()

        # append titles, scores, time, and urls.
        articles.append({
            "title": article["title"],
            "upvotes": article["score"],
            "time": convert_time(article["time"]),
            "url": article["url"],
            })

    return articles

def convert_time(unix_time):
    # convert unix time to data time
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

