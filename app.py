# import the flask modules
from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
import os
import re
# import other pythons scripts
import hackernews_json
import reddit_json
import twitch
import askgpt

# create the application object
app = Flask(__name__)
app.secret_key = 'OifB1@3r8fpPj!ojf2E0'  # set a secret key for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # set session lifetime to 10 min

# default APIs
hackernews_key = "https://hacker-news.firebaseio.com/v0/topstories.json"
reddit_key = "https://www.reddit.com/r/all.json?limit=10"
twitch_key = "cinna"

@app.route('/login', methods=['GET', 'POST'])
# authenticates the user
def login():
    error = None

    #sends the data to the server
    if request.method == 'POST':
        # checks if the username and password are valid
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True  # set a session variable
            session.permanent = True  # set the session to permanent
            return redirect(url_for('frontpage'))  # redirect to the front page if credentials are invalid
        else:
            error = 'Wrong username or password. Please try again.'

    return render_template('login.html', error=error)


@app.route('/')
# uses decorators to link the function to a url
def home():
    return render_template('home.html')

@app.route('/frontpage')
# the main page of the program
def frontpage():
    if not session.get('logged_in'):  # checks if the user is logged in
        return redirect(url_for('login'))  # redirects to login if not logged in

    # requests sort by from the page
    hn_topic = session.get('hn_topic', 'topstories')  # default sort by top
    hackernews_key = f"https://hacker-news.firebaseio.com/v0/{hn_topic}.json"

    subreddit = session.get('reddit_sub', 'all')  # default subreddit
    reddit_key = f"https://www.reddit.com/r/{subreddit}.json?limit=10"

    # parses the json file and returns a list of articles
    hackernews_articles = hackernews_json.parse_hackernews(hackernews_key)
    reddit_posts = reddit_json.parse_reddit(reddit_key)

    # loads twitch stream's ID's
    twitch_streams = twitch.load_streams()

    return render_template(
        # returns all variables that are used on the webpage
        "frontpage.html",
        hackernews_stories=hackernews_articles,
        reddit_posts=reddit_posts,
        twitch_streams=twitch_streams
    )

@app.route('/hackernews_topics', methods=['GET', 'POST'])
# route for Hackers News top articles
def hackernews_topics():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # sort by menu
    topics = {
        'top': 'topstories',
        'new': 'newstories',
        'best': 'beststories',
        'ask': 'askstories',  # ask questions
        'show': 'showstories',  # show personal work
        'jobs': 'jobstories'
    }

    if request.method == 'POST':
        session['hn_topic'] = topics[request.form['topic']]
        return redirect(url_for('frontpage'))
    return render_template('hn_topics.html', topics=topics.keys())

@app.route('/reddit_subreddits', methods=['GET', 'POST'])
# route for Reddit sub choice
def reddit_subreddits():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        session['reddit_sub'] = request.form['subreddit']
        return redirect(url_for('frontpage'))
    return render_template('reddit_subs.html')

@app.route('/add_twitch', methods=['POST'])
def add_twitch():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    stream = request.form['stream']

    # vadlidates input
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        print("Error: Invalid ID")
        return redirect(url_for('frontpage'))

    # adds the new stream
    added = twitch.add_stream(stream)
    if not added:
        print(f"'{stream}' already exists.")

    return redirect(url_for('frontpage'))

@app.route('/delete_twitch/<stream>')
def delete_twitch(stream):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # deletes the stream
    deleted = twitch.delete_stream(stream)
    if not deleted:
        print(f"Stream '{stream}' not found.")

    return redirect(url_for('frontpage'))

@app.route('/askgpt', methods=['GET', 'POST'])
# deploys gemini to parse the user's interests and then fetch the most relevant news articles
def askgpt_route():
    if request.method == 'POST':
        # ask for the user's interests
        user_interests = request.form['interests']
        # retreives top 100 news articles
        all_articles = askgpt.parse_hackernews("https://hacker-news.firebaseio.com/v0/topstories.json")[:100]
        # displays the top 5 articles
        top_5_articles = askgpt.get_summary(user_interests, all_articles) 
        
        return render_template('askgpt_results.html', articles=top_5_articles, interests=user_interests)
    return render_template('askgpt.html')

@app.route('/logout')
# route for logging out of the session
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
