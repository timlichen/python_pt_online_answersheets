from flask_sqlalchemy import SQLAlchemy	
from config import db, likes_table

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_content = db.Column(db.String(255))
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    users_who_like_this_tweet = db.relationship('User', secondary=likes_table)