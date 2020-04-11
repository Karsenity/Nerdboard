from flask import Flask, render_template, request, url_for, redirect
import os

#from src.common.database import Database
#from src.models.trailer import Trailer

from common.database import Database
from models.trailer import Trailer



app = Flask(__name__)


@app.before_first_request
def initialize_database():
    Database.initialize()


uploads_dir = os.path.join(app.root_path, 'static/submissions/trailers')


@app.route('/')
def display_page():
    files = [f for f in os.listdir(uploads_dir) if f != '.DS_Store']
    video_urls = [url_for('static', filename='submissions/trailers/' + url) for url in files]

    return render_template("display.html", len=len(video_urls), videos=video_urls)
    return "<h1>Welcome to Geeks for Geeks</h1>"
