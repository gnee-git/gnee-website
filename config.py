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
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/{}'.format(settings['DATABASE_NAME'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Cloud Storage Configuration
    GCS_BUCKET_NAME = settings['GCS_BUCKET_NAME']
    GCS_PROJECT_ID = settings['GCS_PROJECT_NAME']  # Replace with your project ID
    GCS_DATABASE_FILE = settings['GCS_DATABASE_NAME']  # Name of the SQLite file in GCS

    # Create a Google Cloud Storage client
    storage_client = storage.Client(project=GCS_PROJECT_ID)
    bucket = storage_client.bucket(GCS_BUCKET_NAME)

