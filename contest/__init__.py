from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from sqlalchemy import create_engine
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=""

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
#login_manager=LoginManager(app)
#login_manager.login_view = "login_page"
#login_manager.login_message_category="info"
from contest import routes