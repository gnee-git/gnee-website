from database.models import db, Post

def get_photos():
    return Post.query.filter_by(post_type='photography').order_by(Post.date_time.desc()).all()

def get_blog_posts():
    return Post.query.filter_by(post_type='blog').order_by(Post.date_time.desc()).all()
