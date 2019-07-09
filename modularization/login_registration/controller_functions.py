from flask import render_template, redirect, request, session
from config import db
from models import User

def index():
    return render_template("index.html")

def login():
    is_valid = User.validate_login(request.form)
    if is_valid:
        return redirect("/welcome")
    else:
        return redirect("/")
    
def register():
    is_valid = User.validate_registration(request.form)
    if is_valid:
        new_user = User.add_new_user(request.form)
        session["user_id"] = new_user.id
        return redirect("/welcome")
    else:
        return redirect("/")

def welcome():
    if 'user_id' not in session:
        return redirect("/")
    else:
        logged_in = User.query.get(session["user_id"])
        return render_template("welcome.html", user=logged_in)

def logout():
    session.clear()
    return redirect("/")