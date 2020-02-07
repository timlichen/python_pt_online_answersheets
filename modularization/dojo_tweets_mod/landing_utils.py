from flask import session
from datetime import datetime
from models.user import User

def prep_landing():
    user = User.query.get(session['user_id'])
    tweets = []
    u_f = user.users_this_user_is_following
    for u in u_f:
        tweets.extend(u.user_tweets)
    tweets.extend(user.user_tweets)
    liked_tweets = user.tweets_this_user_likes
    return user, tweets, liked_tweets

def tweet_time(tweets):
    for tweet in tweets:
        td = datetime.utcnow() - tweet.created_at
        if td.seconds == 0:
            tweet.time_since_secs = 1
        if td.seconds < 60 and td.seconds > 0:
            tweet.time_since_secs = td.seconds
        if td.seconds < 3600:
            tweet.time_since_minutes = round(td.seconds / 60) % 60
        if td.seconds > 3600:
            tweet.time_since_hours = round(td.seconds / 3600)
        if td.days > 0:
            tweet.time_since_days = td.days

    return tweets

def tweet_like_count(tweets):
    for tweet in tweets:
        tweet.like_count = len(tweet.users_who_like_this_tweet)
    
    return tweets