from contest import app
from flask import render_template, redirect,url_for, flash, request
from flask_login import login_user,logout_user, login_required, current_user
import os
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

#app.config['UPLOAD_FOLDER']="/Users/Krishay/PycharmProjects/contestplatform/contest/uploads"
#app.config['UPLOAD_FOLDER']="/uploads"
@app.route("/create", methods=["GET","POST"])
def create_page():
    if request.method=="POST":
        if request.files:
            file=request.files['file']
            #file.save(os.path.join(app.config['UPLOAD_FOLDER']),file.filename)
            return redirect(request.url)


    return render_template("create.html")