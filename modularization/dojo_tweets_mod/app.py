from flask import render_template, redirect, flash, request, session
from datetime import datetime, timedelta
from config import app, db, migrate, bcrypt, EMAIL_REGEX
from models.user import User
from models.tweet import Tweet
from landing_utils import tweet_like_count, tweet_time, prep_landing

@app.route("/")
def login_registration_landing():
    return render_template("login_registration.html")

@app.route("/register", methods=['POST'])
def register_user():

    if not User.validate(request.form):
        return redirect("/")
    else:
        encrypted_pw = bcrypt.generate_password_hash(request.form['pw'])
        user = User(first_name=request.form['fn'], last_name=request.form['ln'], 
        email=request.form['em'], password=encrypted_pw)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect("/tweets_landing")
        # all passed info is validated


@app.route("/login", methods=['POST'])
def login_user():
    is_valid = True
    if not request.form['em']:
        is_valid = False
        flash("Please enter an email.")
    
    if not EMAIL_REGEX.match(request.form['em']):
        is_valid = False
        flash("Please enter a valid email.")
    
    if not is_valid:
        return redirect("/")
    else:
        user_list = User.query.filter_by(email=request.form['em']).all()
        
        if not user_list:
            flash("Email is not valid")
            return redirect("/")
        else:
            user = user_list[0]

        if not request.form['pw']:
            is_valid = False
            flash("Please enter a password")

        if not bcrypt.check_password_hash(user.password, request.form['pw']):
            is_valid = False
            flash("Password is not valid")

        if is_valid:
            session['user_id'] = user.id
            return redirect("/tweets_landing")
        else:
            return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/tweets_landing")
def tweet_landing():
    if 'user_id' not in session:
        return redirect("/")

    user, tweets, liked_tweets = prep_landing()
    tweet_time(tweets)
    tweet_like_count(tweets)
        
    if user:
        return render_template("tweet_landing.html", user_data=user, tweet_data=tweets, liked_tweets=liked_tweets)
    else:
        return redirect("/")

@app.route("/tweets_landing_v2")
def tweet_landing_v2():
    if 'user_id' not in session:
        return redirect("/")

    user, tweets, liked_tweets = prep_landing()
    tweet_time(tweets)
    tweet_like_count(tweets)
        
    if user:
        return render_template("fragments/tweet_body.html", tweet_data=tweets, liked_tweets=liked_tweets)
    else:
        return redirect("/")

@app.route("/process_tweet", methods=["POST"])
def validate_proc_tweet():
    is_valid = True

    if not request.form['tweet_content']:
        flash("You cannot post a empty tweet.")
        is_valid = False
    if len(request.form['tweet_content']) > 255:
        flash("Tweets must be less than 255 characters.")
        is_valid = False

    if is_valid:
        tweet = Tweet(content=request.form['tweet_content'], 
        author_id=session['user_id'])
        db.session.add(tweet)
        db.session.commit()
        tweet_like_count([tweet])
        return render_template('fragments/tweet_content.html', tweet=tweet)
    else:
        return "False"
        
    # return redirect("/tweets_landing")

@app.route("/like_tweet/<tweet_id>")
def on_like(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    user = User.query.get(session['user_id'])
    user.tweets_this_user_likes.append(tweet)
    db.session.commit()
    
    return redirect("/tweets_landing")

@app.route("/unlike_tweet/<tweet_id>")
def on_unlike(tweet_id):
    user = User.query.get(session['user_id'])
    tweet = Tweet.query.get(tweet_id)
    user.tweets_this_user_likes.remove(tweet)
    db.session.commit()
    return redirect("/tweets_landing")

@app.route("/delete_tweet/<tweet_id>")
def on_delete(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    db.session.delete(tweet)
    db.session.commit()

    return redirect("/tweets_landing")

@app.route("/tweet_details/<tweet_id>")
def tweet_details(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return redirect("/tweets_landing")
    else:
        user_who_have_liked = tweet.users_who_like_this_tweet
    return render_template("tweet_details.html", tweet=tweet, user_who_have_liked=user_who_have_liked)

@app.route("/on_update/<tweet_id>", methods=['POST'])
def update_tweet(tweet_id):
    tweet = Tweet.query.get(tweet_id)
    tweet.content = request.form['content']
    db.session.commit()
    return redirect(f"/tweet_details/{tweet_id}")

@app.route("/users_to_follow")
def users_to_follow():
    user = User.query.get(session['user_id'])
    all_users = User.query.filter(User.id != user.id).all()
    users_to_follow = [u for u in all_users if u not in user.users_this_user_is_following]
    return render_template("users_to_follow.html", users_to_follow=users_to_follow)
    # users_to_follow

@app.route("/follow_user/<user_id>")
def follow_this_user(user_id):
    user_to_follow = User.query.get(user_id)
    signed_in_user = User.query.get(session['user_id'])
    signed_in_user.users_this_user_is_following.append(user_to_follow)
    db.session.commit()
    return redirect("/tweets_landing")

@app.route("/followers")
def followers():
    followed_users = User.query.get(session['user_id']).users_this_user_is_following
    return render_template("followers.html", followed_users=followed_users)

@app.route("/unfollow/<u_id>")
def on_unfollow(u_id):
    user_to_unfollow = User.query.get(u_id)
    user = User.query.get(session['user_id'])
    user.users_this_user_is_following.remove(user_to_unfollow)
    db.session.commit()
    return redirect("/followers")
    

if __name__ == '__main__':
    app.run(debug=True)