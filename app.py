from flask import Flask, render_template, url_for
from database.db_utils import get_photos, get_blog_posts
from create_db import db
from config import Config
from google.cloud import storage
import os
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

# Ignore the app.context - let's find the database file using the google cloud storage client 
GCS_BUCKET_NAME = settings['GCS_BUCKET_NAME']
GCS_PROJECT_ID = settings['GCS_PROJECT_NAME']  # Replace with your project ID
GCS_DATABASE_FILE = settings['GCS_DATABASE_NAME']  # Name of the SQLite file in GCS

# Initialize Google Cloud Storage client
storage_client = storage.Client(project=GCS_PROJECT_ID)
bucket = storage_client.bucket(GCS_BUCKET_NAME)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app, loading the sqlite file from GCS_DATABASE_FILE if it exists
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]):
    blob = bucket.blob(GCS_DATABASE_FILE)
    blob.download_to_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])



db.init_app(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photography')
def photography():
    photos = get_photos()
    return render_template('photography.html', photos=photos)

@app.route('/blog')
def blog():
    posts = get_blog_posts()
    return render_template('blog.html', posts=posts)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/professional')
def professional():
    return render_template('professional.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
