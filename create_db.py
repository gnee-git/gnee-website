import os
import json
import datetime
from flask import Flask
from google.cloud import storage
from flask_sqlalchemy import SQLAlchemy
from config import Config
import random
# import sqlite3

with open('settings.json', 'r') as f:
    settings = json.load(f)



# Create a Flask app instance (but don't run it)
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy(app)
# db.init_app(app)

# Define the Post model
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    post_type = db.Column(db.String(10), nullable=True)
    photography_url = db.Column(db.String(255), nullable=True)
    photography_comment = db.Column(db.Text, nullable=True)
    blog_title = db.Column(db.String(255), nullable=True)
    blog_text = db.Column(db.Text, nullable=True)

    def __init__(self, post_type, photography_url=None, photography_comment=None, blog_title=None, blog_text=None):
        # generate a random 4 digit integer for the id
        self.id = random.randint(1000, 9999)
        self.date_time = datetime.datetime.now()
        self.post_type = post_type
        self.photography_url = photography_url
        self.photography_comment = photography_comment
        self.blog_title = blog_title
        self.blog_text = blog_text

    def __repr__(self):
        return '<Post {}>'.format(self.id)


# Ignore the app.context - let's find the database file using the google cloud storage client 
GCS_BUCKET_NAME = settings['GCS_BUCKET_NAME']
GCS_PROJECT_ID = settings['GCS_PROJECT_NAME']  # Replace with your project ID
GCS_DATABASE_FILE = settings['GCS_DATABASE_NAME']  # Name of the SQLite file in GCS

# Create an application context
with app.app_context():
    db.create_all()

    # Check whether the database file exists in the Google Cloud Storage bucket - if it does, download it
    storage_client = storage.Client(project=GCS_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_DATABASE_FILE)

    if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1]):
        blob.download_to_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])

    # posts = db.session.query(Post).all()
    # for row in posts:
    #     post = Post(post_type=row.post_type, photography_url=row.photography_url, 
    #                 photography_comment=row.photography_comment, blog_title=row.blog_title, 
    #                 blog_text=row.blog_text)
    #     db.session.add(post)
    # db.session.commit()


    # Create a dummy post, that has none for all fields
    post = Post( post_type='none', photography_url=None, photography_comment=None, blog_title=None, blog_text=None)
    db.session.add(post)
    db.session.commit()

    # save this to the sqlite file
    db.session.commit()
    db.session.close()


    # # # now check the database file exists and has a post in it
    # conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM post")
    # rows = cursor.fetchall()

    # for row in rows:
    #     print(row)

    # # close the connection to the database
    # conn.close()

    # Initialize Google Cloud Storage client
    storage_client = storage.Client(project=GCS_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_DATABASE_FILE)



    # blob.upload_from_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])



