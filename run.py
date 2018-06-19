from flask import Flask, request
import urllib3, urllib.parse

APP_DOMAIN = "flasksubdomain"
CUSTOMERS = ["subdomain"]

app = Flask(__name__)

@app.before_request
def check_subdomain():
    subdomain = urllib.parse.urlsplit(request.url).netloc.split('.')[0]
    path = urllib.parse.urlsplit(request.url).path[:7]
    if (subdomain == APP_DOMAIN and path != '/static'):
        return splash()
    if (subdomain not in CUSTOMERS and path != '/static'):
        abort(404)

@app.route('/')
def index():
    return "this is the application!"

def splash():
    return "here's your splash page!"

app.run(debug=True)