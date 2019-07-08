from flask import render_template, redirect, request
from config import db
from models import Dojo, User

def index():
    all_dojos = Dojo.query.all()
    return render_template("index.html", dojos=all_dojos)

def create_dojo():
    new_dojo = Dojo(name=request.form['name'], city=request.form['city'], state=request.form['state'])
    db.session.add(new_dojo)
    db.session.commit()
    return redirect('/')

def create_ninja():
    new_ninja = User(first_name=request.form['first_name'], last_name=request.form['last_name'], dojos_id=int(request.form['dojo']))
    db.session.add(new_ninja)
    db.session.commit()
    return redirect('/')