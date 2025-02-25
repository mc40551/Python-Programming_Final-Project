https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
https://www.datacamp.com/tutorial/making-http-requests-in-python
https://coolors.co/123524-0a8047-381f04-633605-f78e1e

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
- created styles.css sheet for css styling
- changed the theme to night mode and designed the color palette based on https://colorffy.com/dark-theme-generator?colors=123524-121212, https://m2.material.io/design/color/dark-theme.html#anatomy


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
- appends each post as dictionary to the Reddit list
- converts unix time to datatime

APIs
- https://github.com/HackerNews/API
- https://www.reddit.com/r/all/top.json

Known issue
- Error retrieving Reddit API
Reddit API Status Code: 429
Reddit API Response: {"message": "Too Many Requests", "error": 429}
Error: Status Code: 429