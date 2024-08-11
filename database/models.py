from flask_sqlalchemy import SQLAlchemy
from config import Config
import datetime

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    post_type = db.Column(db.String(10), nullable=False)
    photography_url = db.Column(db.String(255))
    photography_comment = db.Column(db.Text)
    blog_text = db.Column(db.Text)
