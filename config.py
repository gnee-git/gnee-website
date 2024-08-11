import os
from google.cloud import storage

class Config:
    # Read SECRET_KEY from key.txt
    with open('key.txt', 'r') as f:
        SECRET_KEY = f.read().strip()

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/gnee-database.sqlite'  # Use a temporary file
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Cloud Storage Configuration
    GCS_BUCKET_NAME = 'gnee-website'
    GCS_PROJECT_ID = 'gnee-website'  # Replace with your project ID
    GCS_DATABASE_FILE = 'gnee-database.sqlite'  # Name of the SQLite file in GCS

    # Initialize Google Cloud Storage client
    storage_client = storage.Client(project=GCS_PROJECT_ID)  # Define storage_client here
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
