from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy	
from sqlalchemy.sql import func  
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dojo_tweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "burrito"

likes_table = db.Table('likes', 
              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
              db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id'), primary_key=True))

follow_table = db.Table('following', 
               db.Column('followed', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
               db.Column('follower', db.Integer, db.ForeignKey('user.id'), primary_key=True))