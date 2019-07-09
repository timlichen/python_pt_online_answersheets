from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.secret_key = '8pLWNR!IRe5$eb@Q0PiDaSi!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_reg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
migrate=Migrate(app, db)

bcrypt = Bcrypt(app)