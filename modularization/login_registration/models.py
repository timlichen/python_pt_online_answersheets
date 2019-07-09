from sqlalchemy.sql import func
from config import db, bcrypt
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<User {self.id}>:  {self.first_name} {self.last_name}'

    @classmethod
    def validate_registration(cls, postData):
        is_valid = True
        if len(postData['first_name']) < 2:
            is_valid = False
            flash("Please enter your first name. A minimum of 2 characters is required.", "register")
        if len(postData['last_name']) < 2:   
            is_valid = False
            flash("Please enter your last name. A minimum of 2 characters is required.", "register")
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']):
            is_valid = False
            flash("Please enter a valid email address.")
        if len(postData['password']) < 8: 
            is_valid = False
            flash("Please enter a valid password. A minimum of 8 characters is required.", "register")
        if postData['pwconf'] != postData['password']:
            is_valid = False
            flash("The passwords you entered do not match. Please try again.", "register")
        return is_valid

    @classmethod
    def validate_login(cls, postData):
        is_valid = True
        if len(postData["password"]) < 8: 
            is_valid = False
            flash("Please enter your password.", "login")

        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData["email"]):
            is_valid = False
            flash("Please enter your mail address.", "login")

        if not is_valid:
            return is_valid

        user_exists = User.query.filter_by(email=postData["email"]).first()
        if user_exists:
            if bcrypt.check_password_hash(user_exists.password, postData["password"]):
                session['user_id'] = user_exists.id
                return is_valid
            else:
                is_valid = False
                flash("You have entered invalid credentials.", "login")
                return is_valid
        else:    
            is_valid = False
            flash("You have entered invalid credentials.", "login")
            return is_valid

    @classmethod
    def add_new_user(cls, postData):
        pw_hash = bcrypt.generate_password_hash(postData['password'])
        new_user = cls(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user