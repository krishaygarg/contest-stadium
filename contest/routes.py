from contest import app, models,forms,db
from contest.forms import LoginForm, RegisterForm,CreateNewForm, MoreOptionsForm,DeleteForm, QuestionForm
from contest.models import User,Contests, Questions
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
@login_required
def my_contests_page():
    if request.method=="POST":
        contesttocreate=Contests(name="New Contest", owner=current_user.id,type="",setup=1)
        db.session.add(contesttocreate)
        db.session.commit()
        current=Contests.query.filter_by(setup=1).first().id
        Contests.query.filter_by(setup=1).first().setup=0
        db.session.commit()
        return redirect(f"/create/{current}")
    ownedcontests=Contests.query.filter_by(owner=current_user.id)

    #print(type(ownedcontests))
    return render_template("my-contests.html",ownedcontests=ownedcontests,CreateNewForm=CreateNewForm())
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
@app.route("/create/<contestid>", methods=['GET','POST'])
def create_page(contestid):

    contest = Contests.query.filter_by(id=contestid).first()

    if contest:
        if request.method == "POST":
            qtocreate = Questions(type="",contest=contest.id, setup=1,position=Questions.query.filter_by(contest=contest.id).count())
            db.session.add(qtocreate)
            db.session.commit()
            current = Questions.query.filter_by(setup=1).first().id
            Questions.query.filter_by(setup=1).first().setup = 0
            db.session.commit()
            return redirect(f"/question/{current}")
        else:
            pass
        questions=Questions.query.filter_by(contest=contest.id)
        return render_template('create.html',CreateNewForm=CreateNewForm(),contest=contest,questions=questions, Questions=Questions,
                               length=(Questions.query.filter_by(contest=contest.id)).count())
    else:
        return render_template('not-found.html')
@app.route("/question/<questionid>", methods=['GET','POST'])
def question_page(questionid):
    form=QuestionForm()
    if request.method=="POST":
            q = form.question.data
            answer = form.answer.data
            question = Questions.query.filter_by(id=questionid).first()
            if q is not None:
                if question.type=="Text":
                    question.question=q
                    db.session.commit()
                    return redirect(f'/create/{Contests.query.filter_by(id=question.contest).first().id}')
                if question.type=="Free Response Question":
                    question.question=q
                    question.answer=answer
                    db.session.commit()
                    return redirect(f'/create/{Contests.query.filter_by(id=question.contest).first().id}')
                return render_template('base.html')
            dd=request.form.get("dropdown")
            if dd in ["Text", "Free Response Question"]:
                question = Questions.query.filter_by(id=questionid).first()
                question.type=dd
                db.session.commit()
                return render_template('question.html', form=form, question=question)
    else:
        question = Questions.query.filter_by(id=questionid).first()
        if Contests.query.filter_by(id=question.contest).first().owner==current_user.id:
            return render_template('question.html', form=form,question=question)
        else:
            return render_template('not-found.html')

@app.route("/moreoptions/<contestid>",methods=['GET','POST'])
def moreoptions_page(contestid):
    form=MoreOptionsForm()
    delete_form=DeleteForm()
    if form.validate_on_submit():
        torename=Contests.query.filter_by(id=contestid).first()
        if torename:
            Contests.query.filter_by(id=contestid).first().name=form.rename.data
        db.session.commit()
        return redirect(url_for("my_contests_page"))

    if delete_form.validate_on_submit():
        deleted_contest=request.form.get('deleted-contest')
        deleted_contest=Contests.query.filter_by(id=deleted_contest).first()
        if deleted_contest:
            db.session.delete(deleted_contest)
            db.session.commit()
        return redirect(url_for("my_contests_page"))
    contest = Contests.query.filter_by(id=contestid).first()
    return render_template('moreoptions.html', contest=contest,form=form,Contests=Contests,delete_form=delete_form)
