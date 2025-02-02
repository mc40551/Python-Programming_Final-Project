https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
https://www.datacamp.com/tutorial/making-http-requests-in-python

Build a website from scratch
- add app.py, tempates folder, and static folder

app.py
- import Flask and render_template
- import Get in the requests library to retrieve data through APIs
- create app as a Flask object
- route url using @app.route('url')
- return all variables that will are used on the webpage

templates
- contain html template of each url
- Flask supports conditions on html using {% for  %}{%endfor%} {% if  %}{%endif%}

static
- import both bootstrap.mini.css and bootstrap.mini.js as style sheets

json

parsing reddit
- use requests to retrieve API from reddit
- add .json after any reddit link to get json files
- use get to get children dictionary(contain posts information)
- append each post as dictionary to the reddit list
- convert unix time to datatime
- 
pasring HackerNews
- retrieve article IDs through the API
- retrieve article information using IDs

APIs
- https://github.com/HackerNews/API
- https://www.reddit.com/r/all/top.json
