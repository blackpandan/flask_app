import requests
from bs4 import BeautifulSoup as bs

# for bs config
def get_site_file(choice):
    half = "https://coursera.org/courses/"
    url = half+choice
    html_file=requests.get(half).text
    soup = bs(html_file, "lxml")
    return soup


# flask imports
import os
from flask import Flask
from flask import render_template as render, request, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path,'web_scrapper.sqlite'))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/', methods=["GET", "POST"])
    def cult():
        if request.method== "GET":
            return render("index.html")
        elif request.method=="POST":
            soup = get_site_file("bitcoin")
            context = soup.find_all('h1')
            return render("index.html", context={context})
    return app
