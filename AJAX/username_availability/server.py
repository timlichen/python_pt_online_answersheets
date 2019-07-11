from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt    

app = Flask(__name__)
app.secret_key = '8uritt0So@pd!$h'
bcrypt = Bcrypt(app) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/username", methods=['POST'])
def username():
    found = False
    mysql = connectToMySQL('users')
    query = "SELECT username from users WHERE users.username = %(user)s;"
    data = { 'user': request.form['username'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('partials/username.html', found=found)  # render a partial and return it


@app.route("/register", methods=["POST"])
def register_user():
    is_valid = True
    
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter your first name. A minimum of 2 characters is required.", "register")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please enter your last name. A minimum of 2 characters is required.", "register")
    if len(request.form['password']) < 8: 
        is_valid = False
        flash("Please enter a valid password. A minimum of 8 characters is required.", "register")
    if request.form['pwconf'] != request.form['password']:
        is_valid = False
        flash("The passwords you entered do not match. Please try again.", "register")
    
    if is_valid:
        mysql = connectToMySQL('users')
        query = "INSERT into users (first_name, last_name, username, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(un)s, %(pass)s, NOW(), NOW())"
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'un': request.form['username'],
            'pass': bcrypt.generate_password_hash(request.form['password'])
        }
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id
        return redirect("/success")
    else:
        return redirect("/")


@app.route("/login", methods=["POST"])
def login_user():
    is_valid = True

    if len(request.form['username']) < 1:
        is_valid = False
        flash("Please enter your username.", "login")
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Please enter your password.", "login")
    
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL('users')
        query = "SELECT * FROM users WHERE users.username = %(un)s"
        data = {
            'un': request.form['username']
        }
        user = mysql.query_db(query, data)
        if user:
            hashed_password = user[0]['password']
            if bcrypt.check_password_hash(hashed_password, request.form['password']):
                session['user_id'] = user[0]['id']
                return redirect("/success")
            else:
                flash("You have entered invalid credentials.")
                return redirect("/")
        else:
            flash("You have entered invalid credentials.")
            return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/success")
def landing():
    if 'user_id' not in session:
        return redirect("/")

    mysql = connectToMySQL('users')
    query = "SELECT * FROM users WHERE users.id = %(id)s"
    data = {'id': session['user_id']}
    user = mysql.query_db(query, data)

    return render_template("landing.html", user=user[0])


if __name__ == "__main__":
    app.run(debug=True)
