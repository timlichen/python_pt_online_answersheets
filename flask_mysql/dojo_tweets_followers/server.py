from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt   
from datetime import datetime 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "burrito"
bcrypt = Bcrypt(app) 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_user():
    is_valid = True
    
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long")
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address")
    
    if is_valid:
        mysql = connectToMySQL('dojo_tweets')
        # build my query
        query = "INSERT into users (fname, lname, password, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(pass)s, %(email)s, NOW(), NOW())"
        # pass revlevant to with my query
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'pass': bcrypt.generate_password_hash(request.form['password']),
            'email': request.form['email']
        }
        # commit the query
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id

        return redirect("/success")
    else: # otherwise, reidrect and show errors
        return redirect("/")

@app.route("/login", methods=["POST"])
def login_user():
    is_valid = True

    if len(request.form['email']) < 1:
        is_valid = False
        flash("Please enter your email")
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Please enter your password")
    
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL('dojo_tweets')
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        data = {
            'email': request.form['email']
        }
        user = mysql.query_db(query, data)
        if user:
            hashed_password = user[0]['password']
            if bcrypt.check_password_hash(hashed_password, request.form['password']):
                session['user_id'] = user[0]['id']
                return redirect("/success")
            else:
                flash("Password is invalid")
                return redirect("/")
        else:
            flash("Please use a valid email address")
            return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/success")
def landing():
    if 'user_id' not in session:
        return redirect("/")

    mysql = connectToMySQL('dojo_tweets')
    query = "SELECT * FROM users WHERE users.id = %(id)s"
    data = {'id': session['user_id']}
    user = mysql.query_db(query, data)

    mysql = connectToMySQL('dojo_tweets')
    query = "SELECT user_being_followed FROM followed_users WHERE user_following = %(id)s"
    data = {'id': session['user_id']}
    followed_users = [user['user_being_followed'] for user in mysql.query_db(query, data)]


    if followed_users:

        mysql = connectToMySQL('dojo_tweets')
        query = "SELECT * FROM users WHERE users.id = %(id)s"
        data = {'id': session['user_id']}
        user = mysql.query_db(query, data)
        
        mysql = connectToMySQL('dojo_tweets')
        query = "SELECT tweets.users_id, tweets.id as tweet_id, users.fname, tweets.content, tweets.created_at, tweets.content, COUNT(tweets_id) as times_liked FROM liked_tweets RIGHT JOIN tweets ON tweets.id = liked_tweets.tweets_id JOIN users ON tweets.users_id = users.id WHERE tweets.users_id IN %(followed_users)s GROUP BY tweets_id ORDER BY tweets.created_at DESC"
        data = {'followed_users' : tuple(followed_users)}
        tweets = mysql.query_db(query, data)
        
        mysql = connectToMySQL('dojo_tweets')
        query = "SELECT * FROM liked_tweets WHERE users_id = %(user_id)s"
        data = {
            'user_id': session['user_id']
        }
        liked_tweets = [tweet['tweets_id'] for tweet in mysql.query_db(query, data)]

        for tweet in tweets:
            print(datetime.now())
            time_since_posted = datetime.now() - tweet['created_at']
            days = time_since_posted.days
            hours = time_since_posted.seconds//3600 
            minutes = (time_since_posted.seconds//60)%60
            
            if tweet['tweet_id'] in liked_tweets:
                tweet['already_liked'] = True
            else:
                tweet['already_liked'] = False

            tweet['time_since_posted'] = (days, hours, minutes)
                                        
        return render_template("landing.html", user=user[0], tweets=tweets)

    return render_template("landing.html", user=user[0], tweets=[])

@app.route("/tweets/create", methods=['POST'])
def save_tweet():
    if 'user_id' not in session:
        return redirect("/")
        
    is_valid = True
    if len(request.form['content']) < 1:
        is_valid = False
        flash('Tweet cannot be blank')
    if len(request.form['content']) >= 256:
        is_valid = False
        flash('Tweet cannot be more than 255 characters')
    
    if is_valid:
        mysql = connectToMySQL('dojo_tweets')
        query = "INSERT INTO tweets (content, users_id, created_at, updated_at) VALUES (%(cont)s, %(id)s, NOW(), NOW())"
        data = {'id': session['user_id'],
                'cont': request.form['content']}
        tweet = mysql.query_db(query, data)
    
    return redirect("/success")

@app.route("/tweets/<tweet_id>/add_like")
def like_tweet(tweet_id):
    query = "INSERT INTO liked_tweets (users_id, tweets_id) VALUES (%(user_id)s, %(tweet_id)s)"
    data = {
        'user_id': session['user_id'],
        'tweet_id': tweet_id
    }
    mysql = connectToMySQL('dojo_tweets')
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/tweets/<tweet_id>/unlike")
def unlike_tweet(tweet_id):
    query = "DELETE FROM liked_tweets WHERE users_id = %(user_id)s AND tweets_id = %(tweet_id)s"
    data = {
        'user_id': session['user_id'],
        'tweet_id': tweet_id
    }
    mysql = connectToMySQL('dojo_tweets')
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/tweets/<tweet_id>/delete")
def delete_tweet(tweet_id):

    # if ON DELETE CASCADE is not set up for tweets DELETE likes first
    query = "DELETE FROM liked_tweets WHERE tweets_id = %(tweet_id)s"
    data = {
        'tweet_id': tweet_id
    }
    mysql = connectToMySQL('dojo_tweets')
    mysql.query_db(query, data)

    query = "DELETE FROM tweets WHERE id = %(tweet_id)s"
    mysql = connectToMySQL('dojo_tweets')
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/tweets/<tweet_id>/edit")
def edit_tweet(tweet_id):
    if 'user_id' not in session:
        flash("You cannot edit tweets that are not yours.")
        return redirect("/")

    query = "SELECT * FROM tweets WHERE id = %(tid)s"
    data = {'tid': tweet_id}
    mysql = connectToMySQL('dojo_tweets')
    result = mysql.query_db(query, data)
    return render_template("edit_tweet.html", tweet = result[0])

@app.route("/tweets/<tweet_id>/update", methods=['POST'])
def update_tweet(tweet_id):
    if 'user_id' not in session:
        flash("You cannot edit tweets that are not yours.")
        return redirect("/")
        
    is_valid = True
    if len(request.form['content']) < 1:
        is_valid = False
        flash('Tweet cannot be blank')
    if len(request.form['content']) >= 256:
        is_valid = False
        flash('Tweet cannot be more than 255 characters')
    
    if is_valid:
        query = "UPDATE tweets SET content = %(cont)s, updated_at = NOW()"
        data = {'cont': request.form['content']}
        mysql = connectToMySQL('dojo_tweets')
        result = mysql.query_db(query, data)
        flash('Tweet successfully updated')
        return redirect("/success")
    else:
       return redirect("/tweets/{}/edit".format(tweet_id)) 

@app.route("/users")
def show_users():
    query = "SELECT * FROM users WHERE id <> %(id)s ORDER BY lname ASC"
    mysql = connectToMySQL('dojo_tweets')
    data = {
        'id': session['user_id']
    }
    users = mysql.query_db(query, data)

    mysql = connectToMySQL('dojo_tweets')
    query = "SELECT user_being_followed FROM followed_users WHERE user_following = %(id)s"
    data = {'id': session['user_id']}
    followed_users = [user['user_being_followed'] for user in mysql.query_db(query, data)]

    return render_template('users.html', users = users, followed_users = followed_users)

@app.route("/follow/<user_id>")
def follow_user(user_id):
    query = "INSERT INTO followed_users (user_following, user_being_followed) VALUES (%(uid)s, %(uid2)s)"
    mysql = connectToMySQL('dojo_tweets')
    data = {
        'uid': session['user_id'],
        'uid2': user_id
    }
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/unfollow/<user_id>")
def unfollow_user(user_id):
    query = "DELETE FROM followed_users WHERE user_following = %(uid)s AND user_being_followed = %(uid2)s"
    data = {
        'uid': session['user_id'],
        'uid2': int(user_id)
    }
    mysql = connectToMySQL('dojo_tweets')
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/follwed_users")
def followed_users():
    query = "SELECT followed_users.user_following, being_followed.fname, being_followed.lname FROM followed_users LEFT JOIN users on followed_users.user_following = users.id LEFT JOIN users as being_followed on followed_users.user_being_followed = being_followed.id WHERE followed_users.user_following = %(uid)s"
    data = {
        'uid': session['user_id'],
    }
    mysql = connectToMySQL('dojo_tweets')
    followed_users = mysql.query_db(query, data)
    return render_template("/followed_users.html", followed_users=followed_users)


if __name__ == "__main__":
    app.run(debug=True)
