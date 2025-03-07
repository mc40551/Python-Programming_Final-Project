import os
import requests
import datetime
import json
from pathlib import Path
import google.generativeai as genai 

# google API key
GOOGLE_API_KEY = "AIzaSyDD93eux1J4Jb4mLyuegbFoquZBsQszAGs"
genai.configure(api_key=GOOGLE_API_KEY)
# chooses the model
model = genai.GenerativeModel('gemini-2.0-flash')

def get_summary(url):
    # generates a brief summary of the content at the given URL

    if not GOOGLE_API_KEY:
        return "No Gogole API key"
    
    # creates a prompt that summaries the article
    prompt = f"You are a friendly and helpful assistant who looks at the following link and gives a very brief 2-sentence description of the content. If you are not able to provide a summary, return 'no summary'.\n URL: {url}"

    try:
        # generates response based on the prompt
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return response.text.strip()
    
    except Exception:
        return "No summary"

def parse_hackernews(hackernews_key):
    # stores the articles in /data, if the stored data is from within the last 15 minutes, uses stored data instead of requesting new data
    
    # extracts sort by
    sort_by = hackernews_key.split('/')[-1].split('.')[0]
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    cache_file = data_dir / f"hackernews_cache_{sort_by}.json"

    # checks if the data is there
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                cache_data = json.load(f)
                if (
                        cache_data['sort_by'] == sort_by and  
                        # checks if sort_by matches
                        (datetime.datetime.now() - datetime.datetime.strptime(
                            cache_data['timestamp'], '%Y-%m-%d %H:%M:%S')).seconds < 900
                ):
                    return cache_data['articles']
        except:
            pass

    # retrieves data
    news_response = requests.get(hackernews_key).json()[:10]
    articles = []
    for article_id in news_response:
        # iterates through article IDs to retrieve article info
        try:
            article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json").json()
            article_url = article.get("url", "")
            summary = get_summary(article_url)
            # adds summary to the data
            articles.append({
                "title": article.get("title", "No title"),
                "upvotes": article.get("score", 0),
                "time": convert_time(article.get("time", 0)),
                "url": article_url,
                "response": summary 
            })
        except Exception:
            continue

    with open(cache_file, "w") as f:
        json.dump({
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "articles": articles
        }, f)

    return articles

def convert_time(unix_time):
    # converts unix time to data time
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

# https://github.com/HackerNews/API
