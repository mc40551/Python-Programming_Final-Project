# import the Flask class from the flask module
from flask import Flask, render_template
# import requests to retrieve data from APIs
import requests
import hackernews_json
import reddit_json

# create the application object
app = Flask(__name__)

# APIs 
hackernews_key = "https://hacker-news.firebaseio.com/v0/topstories.json"
reddit_key = "https://www.reddit.com/r/all/top.json?limit=10"
twitch_key = "https://jsonplaceholder.typicode.com/posts/1"

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('home.html')  # return a string

@app.route('/frontpage')
def frontpage():

    # hackernews API
    hackernews_articles = hackernews_json.parse_hackernews(hackernews_key)
    
    # parse reddit API
    reddit_posts = reddit_json.parse_reddit(reddit_key)
    
    return render_template( 
        # return all variables that will are used on the webpage
        "frontpage.html",
        hackernews_stories = hackernews_articles,
        reddit_posts = reddit_posts,
        twitch_stream = twitch_stream
    )




# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
