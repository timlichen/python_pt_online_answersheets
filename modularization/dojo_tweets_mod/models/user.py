from config import db
from sqlalchemy.sql import func
from flask import flash
from config import EMAIL_REGEX

from werkzeug.exceptions import HTTPException

likes_table = db.Table('likes', 
              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
              db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id'), primary_key=True))

follow_table = db.Table('following', 
               db.Column('followed', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
               db.Column('follower', db.Integer, db.ForeignKey('user.id'), primary_key=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(70))
    tweets_this_user_likes = db.relationship('Tweet', secondary=likes_table, backref="users_who_like_this_tweet")
    
    users_this_user_is_following = db.relationship('User', secondary=follow_table,
                                                           primaryjoin="User.id==following.c.follower",
                                                           secondaryjoin="User.id==following.c.followed")
    users_who_follow_this_user = db.relationship('User', secondary=follow_table,
                                                         primaryjoin="User.id==following.c.followed",
                                                         secondaryjoin="User.id==following.c.follower")

    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def validate(sub_info):
        try:
            is_valid = True

            if len(sub_info['fn']) < 1:
                is_valid = False
                flash("First name cannot be blank.")
            
            if len(sub_info['ln']) < 1:
                is_valid = False
                flash("Last name cannot be blank.")
            
            if len(sub_info['pwasdasd']) < 8:
                is_valid = False
                flash("Password must be at least 7 characters")
            
            if sub_info['pw'] != sub_info['c_pw']:
                is_valid = False
                flash("Passwords must match")
            
            if not EMAIL_REGEX.match(sub_info['em']):
                is_valid = False
                flash("Please use a valid email.")

            return is_valid
        except HTTPException as exc:
            print(f"There has been an except registering a user: {exc}")
