from flask import Flask
from database.models import db, Post
from config import Config
import os

# Create a Flask app instance (but don't run it)
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Create an application context
with app.app_context():
    db.create_all()
    # Download the database from GCS to the temporary file
    blob = app.config['storage_client'].bucket(app.config['GCS_BUCKET_NAME']).blob(app.config['GCS_DATABASE_FILE'])
    blob.download_to_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])
