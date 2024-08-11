import os
import datetime
from tkinter import Tk, Label, Button, Entry, Text, filedialog
from google.cloud import storage
from database.models import db, Post
from flask import Flask
from config import Config
import json

# Get the settings from the settings.json file
with open('settings.json', 'r') as f:
    settings = json.load(f)



# Google Cloud Storage Configuration
GCS_BUCKET_NAME = settings['GCS_BUCKET_NAME']
GCS_PROJECT_ID = settings['GCS_PROJECT_NAME']  # Replace with your project ID
GCS_DATABASE_FILE = settings['GCS_DATABASE_NAME']  # Name of the SQLite file in GCS

# Initialize Google Cloud Storage client
storage_client = storage.Client(project=GCS_PROJECT_ID)
bucket = storage_client.bucket(GCS_BUCKET_NAME)

# Create a Flask app instance (but don't run it)
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

def create_blog_post():
    def save_blog_post():
        content = blog_text.get("1.0", "end-1c")
        post = Post(post_type='blog', blog_text=content)
        with app.app_context():
            db.session.add(post)
            db.session.commit()
            # Upload the updated database to GCS
            blob = storage_client.bucket(GCS_BUCKET_NAME).blob(GCS_DATABASE_FILE)
            blob.upload_from_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])

        blog_window.destroy()

    blog_window = Tk()
    blog_window.title("Create Blog Post")

    Label(blog_window, text="Enter your blog post in Markdown:").pack()
    blog_text = Text(blog_window, height=10, width=50)
    blog_text.pack()

    Button(blog_window, text="Save", command=save_blog_post).pack()
    blog_window.mainloop()


def create_photo_post():
    def submit_photo():
        # Get the comment
        comment = comment_entry.get()

        # Check if a file has been selected
        if file_path:
            # Upload the photo
            blob = bucket.blob(os.path.join('photographs', os.path.basename(file_path)))
            blob.upload_from_filename(file_path)

            # Create the Post object
            photo = Post(post_type='photography', photography_url=blob.public_url, photography_comment=comment)

            # Save to the database
            with app.app_context():
                db.session.add(photo)
                db.session.commit()

                # Upload the updated database to GCS
                blob = storage_client.bucket(GCS_BUCKET_NAME).blob(GCS_DATABASE_FILE)
                blob.upload_from_filename(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])

        # Close the window
        photo_window.destroy()

    photo_window = Tk()
    photo_window.title("Create Photo Post")

    # File selection
    file_path = None  # Initialize file_path to None

    def choose_file():
        nonlocal file_path  # Declare file_path as nonlocal to modify it within the function
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select a photo",
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("all files", "*.*"))
        )

    Label(photo_window, text="Select a photo:").pack()
    Button(photo_window, text="Choose File", command=choose_file).pack()

    # Comment entry
    Label(photo_window, text="Enter a comment:").pack()
    comment_entry = Entry(photo_window)
    comment_entry.pack()

    # Submit button
    Button(photo_window, text="Submit", command=submit_photo).pack()

    photo_window.mainloop()


# Main GUI
root = Tk()
root.title("Populate Database")

Label(root, text="Choose a post type:").pack()

Button(root, text="Blog Post", command=create_blog_post).pack()
Button(root, text="Photo Post", command=create_photo_post).pack()

# Add Exit Button
Button(root, text="Exit", command=root.quit).pack()  # Use root.quit() to exit

root.mainloop()
