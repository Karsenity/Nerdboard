from flask import Flask, render_template, request, url_for, redirect
#from flask_login import LoginManager
import os
import uuid

from src.common.database import Database
from src.models.trailer import Trailer
from src.models.event import Event
#from common.database import Database
#from models.trailer import Trailer
#from models.event import Event

app = Flask(__name__)

#login = LoginManager(app)
#login.login_view = 'admin_login'

@app.before_first_request
def initialize_database():
    # pass
    Database.initialize()


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

    # files = [f for f in os.listdir(uploads_dir) if f != '.DS_Store']
    # video_urls = [url_for('static', filename='submissions/trailers/' + url) for url in files]
    #, len=len(video_urls), videos=video_urls
    events = Event.get_approved()
    trailers = Trailer.get_approved()
    print(trailers)

    return render_template("display.html", events=events, n_events=len(events), trailers=trailers, n_trailers=len(trailers))


# Handles a file upload
@app.route('/submit/trailer/handle-submission', methods=['POST'])
def handle_trailer_submission():
    _id = uuid.uuid4().hex
    author = request.form.get('name')
    email = request.form.get('email')
    display_email = request.form.get('display-email')
    title = request.form.get('title')

    trailer = request.files.get('trailer')
    trailer_path = os.path.join(uploads_dir, str(_id) + ".mp4")
    trailer.save(trailer_path)

    link = request.form.get('link')

    new_post = Trailer(author, email, display_email, title, trailer_path, link, _id)
    new_post.save_to_mongo()

    return redirect(url_for('confirm_submission'))


# Handles a file upload
@app.route('/submit/event/handle-submission', methods=['POST'])
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
    # new_post.approve()

    return redirect(url_for('confirm_submission'))


# Goes to the submission confirmation
@app.route('/submit/confirm')
def confirm_submission():
    return render_template("confirm-submission.html")


# Submit Project
@app.route('/submit/project')
def submit_project():
    return render_template("submit-project.html")


# Submit Event
@app.route('/submit/event')
def submit_event():
    return render_template("submit-event.html")

# Admin Home Page
@app.route('/admin')
def admin():
    return admin_login()

#Admin Login
@app.route('/admin/login')
def admin_login():
    pass

# Trailer Review (Home)
@app.route('/admin/review/projects')
def review_trailers_home():
    return render_template("review-trailers-home.html")

# Trailer Review (Pages)
@app.route('/admin/review/projects/<i>')
#@login_required
def review_trailers(i):
    trailers = Trailer.get_pending()

    if len(trailers) == 0:
        return redirect(url_for('review_trailers_home'))

    first = 0
    last = len(trailers)-1
    i = max(first, min(last, int(i)))
    current = trailers[i]

    return render_template("review-trailers.html", n=len(trailers), current=current, i=i, first=first, last=last)

@app.route('/admin/approve/trailer/<trailer_id>')
def approve_trailer(trailer_id, index=0):
    Trailer.approve(trailer_id)
    return redirect(url_for('review_trailers', i=index))

@app.route('/admin/deny/<trailer_id>', methods=['GET', 'POST'])
def deny_trailer(trailer_id, index=0):
    Trailer.deny(trailer_id)
    return redirect(url_for('review_trailers', i=index))

# Event Review():
@app.route('/admin/review/events')
def review_events():
    events = Event.get_pending()
    print(events)
    return render_template("review-events.html", events=events, n=len(events))

@app.route('/admin/approve/event/<event_id>')
def approve_event(event_id):
    Event.approve(event_id)
    return redirect(url_for('review_events'))

@app.route('/admin/deny/<event_id>')
def deny_event(event_id):
    Event.deny(event_id)
    return redirect(url_for('review_events'))
