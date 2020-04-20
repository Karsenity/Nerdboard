from flask import Flask, render_template, request, url_for, redirect
import os

#from src.common.database import Database
#from src.models.trailer import Trailer
from common.database import Database
from models.trailer import Trailer
from models.event import Event

app = Flask(__name__)


@app.before_first_request
def initialize_database():
    pass
    #Database.initialize()


uploads_dir = os.path.join(app.root_path, 'static/submissions/trailers')

# Home Page (Temp)
@app.route('/')
def home():
    return choose_submission()

# Submission Choice Page
@app.route('/submit')
def choose_submission():
    return render_template("submit.html")

# Display Page
@app.route('/display')
def display_page():
    files = [f for f in os.listdir(uploads_dir) if f != '.DS_Store']
    video_urls = [url_for('static', filename='submissions/trailers/' + url) for url in files]

    return render_template("display.html", len=len(video_urls), videos=video_urls)

# Handles a file upload
@app.route('/handleTrailerSubmission', methods=['POST'])
def handle_trailer_submission():
    author = request.form.get('name')
    email = request.form.get('email')
    display_email = request.form.get('display-email')
    title = request.form.get('title')
    
    trailer = request.files.get('trailer')
    trailer_name = os.path.join(uploads_dir, trailer.filename)
    trailer.save(os.path.join(uploads_dir, trailer_name))
    
    link = request.form.get('link')

    new_post = Trailer(author, email, display_email, title, trailer_name, link)
    new_post.save_to_mongo()

    return redirect(url_for('confirm_submission'))


# Handles a file upload
@app.route('/handleEventSubmission', methods=['POST'])
def handle_event_submission():
    author = request.form.get('name')
    email = request.form.get('email')
    title = request.form.get('title')
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')
    description = request.form.get('description')

    new_post = Event(author, email, title, date, time, location, description)
    new_post.save_to_mongo()

    return redirect(url_for('confirm_submission'))


# Goes to the submission confirmation
@app.route('/confirm-submission')
def confirm_submission():
    return render_template("submit.html")

# Submit Project
@app.route('/submit-project')
def submit_project():
    return render_template("submit-project.html")

# Submit Event
@app.route('/submit-event')
def submit_event():
    return render_template("submit-event.html")

