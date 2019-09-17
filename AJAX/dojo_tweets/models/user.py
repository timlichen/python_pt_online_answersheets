from flask_sqlalchemy import SQLAlchemy	
from config import db, likes_table, follow_table

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    tweets_this_user_likes = db.relationship('Tweet', secondary=likes_table)
    users_this_user_is_following = db.relationship('User', secondary=follow_table,
                                                           primaryjoin="User.id==following.c.follower",
                                                           secondaryjoin="User.id==following.c.followed")
    users_who_follow_this_user = db.relationship('User', secondary=follow_table,
                                                         primaryjoin="User.id==following.c.followed",
                                                         secondaryjoin="User.id==following.c.follower")