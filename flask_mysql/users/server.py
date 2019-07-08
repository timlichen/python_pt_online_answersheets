from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL 
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("add_user.html")

@app.route("/save_user", methods=['POST'])
def commit_user():
    query = "INSERT INTO users (first_name, last_name, email, description, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(dsc)s, NOW(), NOW())"
    data = {
        'fn': request.form['f_name'],
        'ln': request.form['l_name'],
        'em': request.form['email'],
        'dsc': request.form['description']
    }
    mysql = connectToMySQL('users')
    user_id = mysql.query_db(query, data)

    return redirect('/users/{}'.format(user_id))      

@app.route("/users/<user_id>")
def view_user(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = {
        'id': user_id
    }
    mysql = connectToMySQL('users')
    user = mysql.query_db(query, data)
    print(user)
    return render_template("user_details.html", user = user[0])

@app.route("/delete/<user_id>")
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %(id)s"
    data = {
        'id': user_id
    }
    mysql = connectToMySQL('users')
    user = mysql.query_db(query, data)
    return redirect("/users")

@app.route("/edit_user/<user_id>")
def edit_user(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = {
        'id': user_id
    }
    mysql = connectToMySQL('users')
    user = mysql.query_db(query, data)
    return render_template("edit.html", user=user[0])

@app.route("/update_user/<user_id>", methods=['POST'])
def update_user(user_id):
    query = "UPDATE users SET first_name=%(fn)s, last_name=%(ln)s, email=%(em)s, description=%(dsc)s, updated_at=NOW()"
    data = {
      'fn': request.form['f_name'],
      'ln': request.form['l_name'],
      'em': request.form['email'],
      'dsc': request.form['description']
    }
    mysql = connectToMySQL('users')
    mysql.query_db(query, data)
    return redirect('/users/{}'.format(user_id))

@app.route("/users")
def all_users():
    query = "SELECT * FROM users"
    mysql = connectToMySQL('users')
    all_users = mysql.query_db(query)
    print(all_users)
    return render_template("all_users.html", all_users=all_users)
if __name__ == "__main__":
    app.run(debug=True)