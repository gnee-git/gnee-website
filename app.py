from flask import Flask, render_template
from database.db_utils import get_photos, get_blog_posts
from database.models import db
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

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

# ... other routes for music, contact, professional

if __name__ == '__main__':
    app.run(debug=True)
