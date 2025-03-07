https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
https://www.datacamp.com/tutorial/making-http-requests-in-python
https://coolors.co/123524-0a8047-381f04-633605-f78e1e
https://www.planeks.net/open-ai-api-integration-guide/

Build a website from scratch
- added app.py, tempates folder, and static folder

app.py
- Framework: uses Flask to handle routing, request handling, and rendering of HTML templates
- imports Get in the requests library to retrieve data through APIs
- creates app as a Flask object
- uses Flask's `session` object for user login status and stores user preferences
- routes url using @app.route('url')
- routes to a login page that authenticates user credential
- returns all variables that will are used on the webpage
- uses dynamic url to retreive target articles
- for Hackers News, the user can select stories from a drop down menu
- uses Gemini AI to parse user interests and fetch relevant news articles
- for Reddit, the user can enter a subreddit's name
- the secret key contains the credential that protects the session's integrity
- a logged in status is useful to check if a user is logged in
- set the session to permanent and set a expiration time so the logged in status can last through window closing

templates
- contains html template of each url
- Flask supports conditions on html using {% for  %}{%endfor%} {% if  %}{%endif%}
- contains the login page, username: admin, pw: admin

static
- imports both bootstrap.mini.css and bootstrap.mini.js as style sheets
- adds an images folder to host all images that will be used on the website
- created styles.css sheet for css styling
- changed the theme to night mode and designed the color palette based on https://colorffy.com/dark-theme-generator?colors=123524-121212, https://m2.material.io/design/color/dark-theme.html#anatomy

Json py files
Header
- add anchor links of each section that jump to each section
pasring Hacker News
- uses the Hacker News API (`https://github.com/HackerNews/API`) to fetch article IDs and details
- caches fetched articles in `/data` to reduce API calls
- retrieves article IDs through the API
- retrieves article information using IDs
- uses the Gemini AI model to generate a brief 2-sentence summary of each article 
- the return to top link jumps back to the top
parsing Reddit
-uses the Reddit API (`https://www.reddit.com/r/<subreddit>/top.json`) to fetch posts from a specified subreddit
- uses requests to retrieve API from reddit
- adds .json after any reddit link to get json files
- uses get to get children dictionary(contain posts information)
- appends each post as dictionary to the Reddit list
- uses the Gemini AI model to generate a brief 2-sentence summary of each post
- caches retrieved data for repetitive use to avoid too many requests error
- converts unix time to datatime
pasring Twitch
- manages a list of Twitch stream IDs stored
- handles adding and deleting functions

Known issue
- erro when requesting from Reddit too often
Error retrieving Reddit API
Reddit API Status Code: 429
Reddit API Response: {"message": "Too Many Requests", "error": 429}
Error: Status Code: 429

More features
- user registration and maintaince
- database that maintains user info
- pagination function for the Hacker News and Reddit

AIzaSyDD93eux1J4Jb4mLyuegbFoquZBsQszAGs
