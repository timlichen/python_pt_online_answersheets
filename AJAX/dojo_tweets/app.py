from flask import Flask, render_template, session, redirect, request
from config import app
from models.user import User
from models.tweet import Tweet

from mysqlconnection import connectToMySQL
from config import app, db, migrate

@app.route("/")
def index():
    return render_template('login_reg.html')

@app.route("/register", methods=['POST'])
def register():
    if request.form['password'] != request.form['c_password']:
        return redirect("/")
    # mysql = connectToMySQL('dojo_tweets')
    # query = "INSERT INTO users (user_name, password) VALUES (%(un)s, %(pw)s)"
    # data = {
    #     'un': request.form['name'],
    #     'pw': request.form['password']
    # }
    # saved_user_id = mysql.query_db(query, data)
    user = User(user_name=request.form['name'], password=request.form['password'])
    db.session.add(user)
    db.session.commit()

    return redirect('/')
    
    # if saved_user_id:
    #     session['user_id'] = saved_user_id
    #     return redirect("/create_tweet")
    # else:
    #     return redirect('/')

@app.route("/login", methods=['POST'])
def login():
    # mysql = connectToMySQL('dojo_tweets')
    # query = "SELECT * FROM users WHERE user_name = %(un)s"
    # data = {
    #     'un': request.form['name']
    # }
    # user = mysql.query_db(query, data)
    user = User.query.filter_by(user_name=request.form['name']).all()
    if user:
        user = user[0]
        if user.password == request.form['password']:
            session['user_id'] = user.id
            return redirect("/create_tweet")
    return redirect("/")

@app.route("/create_tweet")
def show_create_tweet_page():
    # mysql = connectToMySQL('dojo_tweets')
    # query = "SELECT * from tweets"
    # all_tweets = mysql.query_db(query)
    user = User.query.get(session['user_id'])
    all_followed_users = user.users_this_user_is_following
    followed_tweets = []
    for user in all_followed_users:
        followed_tweets.extend(Tweet.query.filter_by(users_id=user.id).all())

    return render_template('index.html', followed_tweets=followed_tweets)

@app.route("/save_tweet", methods=['POST'])
def save_tweet():
    # mysql = connectToMySQL('dojo_tweets')
    # query = "INSERT INTO tweets (tweet_content, Users_id) VALUES(%(tm)s, %(uid)s)"
    # data = {
    #   'tm': request.form['tweet'],
    #   'uid': session['user_id']  
    # }
    # mysql.query_db(query, data)
    tweet = Tweet(tweet_content=request.form['tweet'], users_id=session['user_id'])
    db.session.add(tweet)
    db.session.commit()

    return redirect("/create_tweet")

@app.route("/tweets/<tweet_id>/delete", methods=['POST'])
def delete_tweet(tweet_id):
    # mysql = connectToMySQL('dojo_tweets')
    # query = "DELETE FROM tweets WHERE id = %(tid)s"
    # data = {
    #     'tid': tweet_id
    # }
    # mysql.query_db(query, data)
    tweet_to_delete = Tweet.query.get(tweet_id)
    db.session.delete(tweet_to_delete)
    db.session.commit()

    return redirect("/create_tweet")

@app.route("/tweets/<tweet_id>/like", methods=['POST'])
def like_tweet(tweet_id):
    # mysql = connectToMySQL('dojo_tweets')
    # query = "INSERT INTO likes (Users_id, Tweets_id) VALUES (%(uid)s, %(tid)s)"
    # data = {
    #     'uid': session['user_id'],
    #     'tid': tweet_id
    # }
    # mysql.query_db(query, data)
    user = User.query.get(session['user_id'])
    tweet = Tweet.query.get(tweet_id)
    user.tweets_this_user_likes.append(tweet)
    db.session.commit()

    return redirect("/create_tweet")

@app.route("/users")
def see_all_users():
    users = User.query.all()
    db.session.commit()

    return render_template("users.html", all_users = users)


@app.route("/get_tweets_async/<user_id>")
def get_tweets_async(user_id):
    user = User.query.get(user_id)
    all_followed_users = user.users_this_user_is_following
    followed_tweets = []
    for user in all_followed_users:
        followed_tweets.extend(Tweet.query.filter_by(users_id=user.id).all())

    return render_template('/partials/just_tweets.html', followed_tweets=followed_tweets)

@app.route("/follow/<user_id>")
def follow_a_user(user_id):
    logged_in_user = User.query.get(session['user_id'])
    user_to_follow = User.query.get(user_id)
    logged_in_user.users_this_user_is_following.append(user_to_follow)
    db.session.commit()
    return redirect("/create_tweet")
if __name__ == '__main__':
    app.run(debug=True)

