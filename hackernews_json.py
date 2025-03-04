import requests
import datetime

def parse_hackernews(hackernews_key):
    # access API
    news_response = requests.get(hackernews_key).json()[:10]
    articles = []
    for article_id in news_response:
        # iterate through article IDs to retreive article info
        try:
            article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json").json()

            # append titles, scores, time, and urls.
            articles.append({
                "title": article.get("title", "No title"), 
                "upvotes": article.get("score", 0), 
                "time": convert_time(article.get("time", 0)),
                "url": article.get("url", ""), 
            })

        except Exception:
            continue 

    return articles

def convert_time(unix_time):
    # convert unix time to data time
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')
