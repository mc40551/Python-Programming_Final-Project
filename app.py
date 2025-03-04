# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session  # Import session
from datetime import timedelta # Import timedelta

# import requests to retrieve data from APIs
import hackernews_json
import reddit_json

# create the application object
app = Flask(__name__)
app.secret_key = 'OifB1@3r8fpPj!ojf2E0'  # set a secret key for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) # set session lifetime to 10 min

# APIs
hackernews_key = "https://hacker-news.firebaseio.com/v0/topstories.json"
reddit_key = "https://www.reddit.com/r/all/top.json?limit=10"
twitch_key = "hasanabi"

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin': 
            session['logged_in'] = True  # set a session variable
            session.permanent = True  # set the session to permanent so it does not end after closing the window
            return redirect(url_for('frontpage'))
        else:
            error = 'Wrong username or password. Please try again.'
    return render_template('login.html', error = error)

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('home.html')  # return a string

@app.route('/frontpage')
def frontpage():
    if not session.get('logged_in'): # check if the user is logged in
        return redirect(url_for('login'))  # redirect to login if not logged in

    # hackernews API
    hackernews_articles = hackernews_json.parse_hackernews(hackernews_key)

    # parse reddit API
    reddit_posts = reddit_json.parse_reddit(reddit_key)

    return render_template(
        # return all variables that will are used on the webpage
        "frontpage.html",
        hackernews_stories = hackernews_articles,
        reddit_posts = reddit_posts,
        twitch_hand = twitch_key
    )

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
