from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt    
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
        mysql = connectToMySQL('login_registration')
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

# 3 set up login
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
        mysql = connectToMySQL('login_registration')
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

    mysql = connectToMySQL('login_registration')
    query = "SELECT * FROM users WHERE users.id = %(id)s"
    data = {'id': session['user_id']}
    user = mysql.query_db(query, data)

    return render_template("landing.html", user=user[0])

if __name__ == "__main__":
    app.run(debug=True)
