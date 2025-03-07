import os
import requests
import datetime
import json
from pathlib import Path
import google.generativeai as genai 

GOOGLE_API_KEY = "AIzaSyDD93eux1J4Jb4mLyuegbFoquZBsQszAGs" 

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Please set it as an environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_summary(url):
    # generates a brief summary of the content at the given URL

    if not GOOGLE_API_KEY:
        return "No Gogole API key"

    prompt = f"You are a friendly and helpful assistant who looks at the following link and gives a very brief 2-sentence description of the content. If you are not able to provide a summary, return 'no summary.\n URL: {url}"
    #print(f"prompt: {prompt} \n")
    #print(f"{url}\n")

    try:
        # generates response based on the prompt
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print(f"Generated Summary: {summary}\n")
        return response.text.strip()
    
    except Exception:

        return "No summary"

def parse_reddit(reddit_key):
    # stores the articles in /data, if the stored data is from within the last 15 minutes, uses stored data instead of requesting new data
    
    #extracts subreddit name
    subreddit = reddit_key.split('/')[4]
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    filename = f"reddit_{subreddit}.json"
    filepath = data_dir / filename

    if filepath.exists():
        with open(filepath) as f:
            try:
                cached = json.load(f)
                if (cached['subreddit'] == subreddit and
                        (datetime.datetime.now() - datetime.datetime.strptime(
                            cached['timestamp'], '%Y-%m-%d %H:%M:%S')).seconds < 900):
                    return cached['posts']
            except Exception:
                pass

    reddit_response = requests.get(reddit_key)

    if reddit_response.status_code != 200:
        print(f"Error fetching Reddit posts. Status Code: {reddit_response.status_code}")
        return []

    reddit_response_json = reddit_response.json()
    data = reddit_response_json.get("data", {})
    children = data.get("children", [])
    
    reddit_posts = []

    for post in children:
        post_data = post.get("data", {})
        if not post_data:
            continue

        post_url = f"https://www.reddit.com{post_data.get('permalink', '')}"
        summary = get_summary(post_url)

        reddit_posts.append({
            "title": post_data.get("title", "No title"),
            "subreddit": post_data.get("subreddit", "Unknown"),
            "upvotes": post_data.get("ups", 0),
            "thumbnail": post_data.get("thumbnail", ""),
            "time": convert_time(post_data.get("created", 0)),
            "id": post_data.get("id", ""),
            "url": f"https://redd.it/{post_data.get('id', '')}",
            "response": summary 
        })

    with open(filepath, 'w') as f:
        json.dump({
            "subreddit": subreddit,
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "posts": reddit_posts
        }, f)

    return reddit_posts

def convert_time(unix_time):
    date_time = datetime.datetime.fromtimestamp(unix_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S')
