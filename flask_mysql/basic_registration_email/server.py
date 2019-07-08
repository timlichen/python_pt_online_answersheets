import re

from flask import Flask, render_template, redirect, flash, request
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "carnitas"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST'])
def register_user():
    is_valid = True
    if len(request.form['fn']) < 1:
        is_valid = False
        flash("First name is a required field")
    if len(request.form['ln']) < 1:
        is_valid = False
        flash("Last name is a required field")
    if len(request.form['password']) <= 5:
        is_valid = False
        flash("Password must be at least 5 characters long")
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match")
    if not request.form['fn'].isalpha():
        is_valid = False
        flash("First name can only contain alphabetic chracters")
    if not request.form['ln'].isalpha():
        is_valid = False
        flash("First name can only contain alphabetic chracters")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Email cannot be blank!")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid Email Address!")
        
    if is_valid:
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s)"
        data = {
            'fn': request.form['fn'],
            'ln': request.form['ln'],
            'em': request.form['email'],
            'pw': request.form['password']
        }
        mysql = connectToMySQL('basic_registration')
        result_id = mysql.query_db(query, data)
        flash("Sucessfully inserted user: {}".format(result_id))
    
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)