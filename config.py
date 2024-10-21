import os
from google.cloud import storage
import json

# Get the settings from the settings.json file
with open('settings.json', 'r') as f:
    settings = json.load(f)



class Config:
    # Read SECRET_KEY from key.txt
    with open('key.txt', 'r') as f:
        SECRET_KEY = f.read().strip()

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/{}'.format(settings['GCS_DATABASE_NAME'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set the database configuration to be the Google Cloud Storage location

    # Google Cloud Storage Configuration
    GCS_BUCKET_NAME = settings['GCS_BUCKET_NAME']
    GCS_PROJECT_ID = settings['GCS_PROJECT_NAME']  # Replace with your project ID
    GCS_DATABASE_FILE = settings['GCS_DATABASE_NAME']  # Name of the SQLite file in GCS

    # Initialize Google Cloud Storage client
    storage_client = storage.Client(project=GCS_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)

    # Now download the database file from GCS if it doesn't exist
    if not os.path.exists(SQLALCHEMY_DATABASE_URI.split('///')[1]):
        blob = bucket.blob(GCS_DATABASE_FILE)
        blob.download_to_filename(SQLALCHEMY_DATABASE_URI.split('///')[1])