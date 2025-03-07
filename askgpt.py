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

def get_interest(user_response):
    # generates a brief summary of the content at the given URL

    if not GOOGLE_API_KEY:
        return "No Gogole API key"
    
    # creates a prompt that analyzes the user's response and output keywords
    prompt = f"User Response: {user_response} Analyze the user's response and extract the top 3-5 keywords representing their primary interests. Provide the keywords as a comma-separated list. Keywords:'"
    
    try:
        # generates response based on the prompt
        response = model.generate_content(prompt)
        # keywords of the user's interests
        interests = response.text.strip()
        return interests
    
    except Exception:
        return ""

def get_summary(interests, articles):
    #filters and ranks articles based on the user's interests

    if not GOOGLE_API_KEY:
        return "No Gogole API key"
    
    prompt = f"Given the user's interests: '{interests}', select the top 5 articles from the following list that are most relevant. If you are not able to answer the prompt, return the error reason:\n\n"
    # adds all articles
    for article in articles:
        prompt += f"- {article['title']}: {article['url']}\n"
    prompt += "\nReturn and format the entire response as a string, provide article title, article url, and a very brief 2-sentence description of the content. If you are not able to provide a summary, return 'no summary'."

    try:
        response = model.generate_content(prompt)
        results = response.text.strip()
        print(f"result: {results}")
        return results
    except Exception:
        return ""

def parse_hackernews(hackernews_key):
    # stores the articles in /data, if the stored data is from within the last 15 minutes, uses stored data instead of requesting new data
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    cache_file = data_dir / "hackernews_cache_ask.json"
    # checks if the data is there
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                cache_data = json.load(f)
                if (datetime.datetime.now() - datetime.datetime.strptime(
                        cache_data['timestamp'], '%Y-%m-%d %H:%M:%S')).seconds < 900:
                    return cache_data['articles']
        except:
            pass

    # retrieves data
    news_response = requests.get(hackernews_key).json()[:100]
    articles = []
    for article_id in news_response:
        # iterates through article ID's to retrieve article info
        try:
            article = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json").json()
            article_url = article.get("url", "")
            # adds summary to the data
            articles.append({
                "title": article.get("title", "No title"),
                "upvotes": article.get("score", 0),
                "time": convert_time(article.get("time", 0)),
                "url": article_url,
                "response": "" 
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
