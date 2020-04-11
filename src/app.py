from flask import Flask, render_template, request, url_for, redirect
import os

#from src.common.database import Database
#from src.models.trailer import Trailer

#from common.database import Database
#from models.trailer import Trailer



app = Flask(__name__)


@app.before_first_request
def initialize_database():
    pass
    #Database.initialize()


uploads_dir = os.path.join(app.root_path, 'static/submissions/trailers')


@app.route('/')
def display_page():
    files = [f for f in os.listdir(uploads_dir) if f != '.DS_Store']
    video_urls = [url_for('static', filename='submissions/trailers/' + url) for url in files]

    return render_template("display.html", len=len(video_urls), videos=video_urls)

# Handles a file upload
@app.route('/handleUpload', methods=['POST'])
def handle_file_upload():
    # Imagine we were given the info below from the website when we got the request with photo
    author = "John Doe"
    email = "john.doe18@ncf.edu"
    aoc = "Comp Sci"
    title = "Sample Title"
    summary = "this is a sample database entry"

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.save(os.path.join(uploads_dir, photo.filename))
            new_post = Trailer(author, email, aoc, title, summary)
            Trailer.save_to_mongo(new_post)

    return redirect(url_for('upload_file'))

# Submission Choice Page
@app.route('/submit')
def choose_submission():
    return render_template("submit.html")

# Submit Project
@app.route('/submit-project')
def submit_project():
    return render_template("submit-project.html")

# Submit Event
@app.route('/submit-event')
def submit_event():
    return render_template("submit-event.html")

