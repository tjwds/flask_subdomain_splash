# Flask subdomains

Curious about how to handle subdomains with Flask?  Read on!

tl;dr: Just check out `run.py`, it's pretty straight-forward.

## set up environment

Add the following lines to your hosts file:

```
127.0.0.1       flasksubdomain.test
127.0.0.1       subdomain.flasksubdomain.test
```

You'd use a wildcard A record for your application in development, but this will do for now.  You'll also need `flask` and `urllib3`.  Clone this repo, then run `python3 run.py`!

## the code, with comments

```python
from flask import Flask, request
import urllib3, urllib.parse

# Your URL without subdomains or TLD and a list of valid subdomains.  
# A good application here is if you have a sign-up view which writes to a database of subdomains.
APP_DOMAIN = "flasksubdomain"
CUSTOMERS = ["subdomain"]

app = Flask(__name__)

# Before each app request,
@app.before_request
def check_subdomain():
  	# Use URLlib to parse the request URL and get the subdomain and hierarchical path.
    # path checks to see if static items are being requested and lets them through.  
    # Change this if you're changing the flask default static directory.
    subdomain = urllib.parse.urlsplit(request.url).netloc.split('.')[0]
    path = urllib.parse.urlsplit(request.url).path[:7]
    # return the splash page if no subdomain
    if (subdomain == APP_DOMAIN and path != '/static'):
        return splash()
    # return a 404 if an invalid subdomain is requested
    # if you want to test this locally, you'll have to add to your hosts file!
    if (subdomain not in CUSTOMERS and path != '/static'):
        abort(404)

# Add routes like any other application.
@app.route('/')
def index():
    return "this is the application!"

# Here's your splash function, just without the app decorator. 
# In my application, this is just serving a react app: render_template('splash.html')
def splash():
    return "here's your splash page!"

# It goes without saying, but don't use the flask dev server in production, and especially don't use it with debug set to True!
app.run(debug=True)
```


