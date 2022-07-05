from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from sqlalchemy import create_engine
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://ypnfuyfujgihxl:8765715414a3c841159e5191bdb75821e6b5a322b234befcf92416f0b7d992ac@ec2-54-157-16-196.compute-1.amazonaws.com:5432/dclfnqjdv9gjhm"
app.config['SECRET_KEY']=('f104e32cea94bb2106e6118a')
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category="info"
from contest import routes,models
db.drop_all()
db.create_all()
