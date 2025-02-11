https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
https://www.datacamp.com/tutorial/making-http-requests-in-python

Build a website from scratch
- added app.py, tempates folder, and static folder

app.py
- imports Flask and render_template
- imports Get in the requests library to retrieve data through APIs
- creates app as a Flask object
- routes url using @app.route('url')
- returns all variables that will are used on the webpage

templates
- contains html template of each url
- Flask supports conditions on html using {% for  %}{%endfor%} {% if  %}{%endif%}

static
- imports both bootstrap.mini.css and bootstrap.mini.js as style sheets
- adds an images folder to host all images that will be used on the website

json

Header
- add anchor links of each section that jump to each section

pasring HackerNews
- retrieves article IDs through the API
- retrieves article information using IDs
- the return to top link jumps back to the top

parsing reddit
- uses requests to retrieve API from reddit
- adds .json after any reddit link to get json files
- uses get to get children dictionary(contain posts information)
- appends each post as dictionary to the reddit list
- converts unix time to datatime

APIs
- https://github.com/HackerNews/API
- https://www.reddit.com/r/all/top.json
