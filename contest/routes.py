from contest import app, models,forms,db
from contest.forms import LoginForm, RegisterForm
from contest.models import User
from flask import render_template, redirect,url_for, flash, request
from flask_login import login_user,logout_user, login_required, current_user
import os
@app.route("/")
@app.route("/home")
def home_page():
    users=User.query.all()
    return render_template("home.html",users=users)

#app.config['UPLOAD_FOLDER']="/Users/Krishay/PycharmProjects/contestplatform/contest/uploads"
#app.config['UPLOAD_FOLDER']="/uploads"

@app.route("/my-contests", methods=["GET","POST"])
def my_contests_page():
    if request.method=="POST":
        if request.files:
            file=request.files['file']
            #file.save(os.path.join(app.config['UPLOAD_FOLDER']),file.filename)
            return redirect(request.url)


    return render_template("my-contests.html")
@app.route("/register", methods=['GET','POST'])
def register_page():
    form=RegisterForm()

    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('my_contests_page'))
    if (form.errors!={}):
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}',category='success')
            return redirect(url_for('my_contests_page'))
        else:
            flash('Invalid username and/or password. Please try again',category='danger')
    return render_template('login.html',form=form)
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been successfully logged out!", category="info")
    return redirect(url_for("home_page"))