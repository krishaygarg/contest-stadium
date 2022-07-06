from contest import app, models,forms,db
from contest.forms import LoginForm, RegisterForm,CreateNewForm, MoreOptionsForm,DeleteForm, QuestionForm,MoveUpForm
from contest.forms import MoveDownForm, ReleaseForm, CodeForm, EnterForm, ContestForm
from contest.models import User,Contests, Questions, Results
from flask import render_template, redirect,url_for, flash, request
from flask_login import login_user,logout_user, login_required, current_user
from wtforms import StringField
import random, time
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
        contesttocreate=Contests(name="New Contest", owner=current_user.id,type="",setup=1,time=3600)
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
        next_url=request.form.get("next")
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}',category='success')
            if next_url:
                return redirect(next_url)
            else:
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
    MoveUp=MoveUpForm()
    MoveDown=MoveDownForm()
    contest = Contests.query.filter_by(id=contestid).first()

    if contest:
        if request.method == "POST":

            if MoveUp.submit2.data and MoveUp.validate():
                tomoveup=int(request.form.get('tomoveup'))
                print(Questions.query.filter_by(position=tomoveup, contest=contestid).first().question)
                idtochange=Questions.query.filter_by(position=tomoveup, contest=contestid).first().id
                idtochange1 = Questions.query.filter_by(position=tomoveup-1, contest=contestid).first().id
                Questions.query.filter_by(id=idtochange).first().position-=1
                Questions.query.filter_by(id=idtochange1).first().position+=1
                db.session.commit()
                print(Questions.query.filter_by(position=tomoveup, contest=contestid).first().question)

                return redirect(request.url)
            if MoveDown.submit3.data and MoveDown.validate():
                tomovedown = int(request.form.get('tomovedown'))
                idtochange = Questions.query.filter_by(position=tomovedown, contest=contestid).first().id
                idtochange1 = Questions.query.filter_by(position=tomovedown + 1, contest=contestid).first().id
                Questions.query.filter_by(id=idtochange).first().position += 1
                Questions.query.filter_by(id=idtochange1).first().position -= 1
                db.session.commit()
                return redirect(request.url)
            if CreateNewForm().submit1.data and CreateNewForm().validate():
                qtocreate = Questions(type="",contest=contest.id, setup=1,position=Questions.query.filter_by(contest=contest.id).count(),
                                      question="", answer="")
                db.session.add(qtocreate)
                db.session.commit()
                current = Questions.query.filter_by(setup=1).first().id
                Questions.query.filter_by(setup=1).first().setup = 0
                db.session.commit()
                return redirect(f"/question/{current}")
        if request.method=="GET":
            pass
        questions=Questions.query.filter_by(contest=contest.id)
        return render_template('create.html',CreateNewForm=CreateNewForm(),contest=contest,questions=questions, Questions=Questions,
                               length=(Questions.query.filter_by(contest=contest.id)).count(),MoveUp=MoveUp,MoveDown=MoveDown)
    else:
        return render_template('not-found.html')
@app.route("/question/<questionid>", methods=['GET','POST'])
def question_page(questionid):
    form=QuestionForm()
    delete_form=DeleteForm()
    question = Questions.query.filter_by(id=questionid).first()
    if request.method=="POST":
            if delete_form.validate_on_submit():
                deleted_question = request.form.get('deleted-question')
                deleted_question = Questions.query.filter_by(id=deleted_question).first()
                if deleted_question:

                    for element in Questions.query.filter_by(contest=deleted_question.contest):
                        element.position-=1
                    db.session.delete(deleted_question)
                    db.session.commit()
                return redirect(f"/create/{Contests.query.filter_by(id=question.contest).first().id}")
            q = form.question.data
            answer = form.answer.data

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
                return render_template('question.html', form=form, question=question, delete_form=delete_form)
    else:
        question = Questions.query.filter_by(id=questionid).first()
        if Contests.query.filter_by(id=question.contest).first().owner==current_user.id:
            return render_template('question.html', form=form,question=question,delete_form=delete_form)
        else:
            return render_template('not-found.html')

@app.route("/moreoptions/<contestid>",methods=['GET','POST'])
def moreoptions_page(contestid):
    form=MoreOptionsForm()
    delete_form=DeleteForm()
    if form.save.data and form.validate():

            torename=Contests.query.filter_by(id=contestid).first()
            if torename:
                Contests.query.filter_by(id=contestid).first().name=form.rename.data
                Contests.query.filter_by(id=contestid).first().time = form.timehrs.data*3600+form.timemins.data*60+form.timesecs.data
            db.session.commit()
            return redirect(url_for("my_contests_page"))
    elif (form.errors != {}):
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')
    if request.form.get('deleted-contest'):
        deleted_contest=request.form.get('deleted-contest')
        deleted_contest=Contests.query.filter_by(id=deleted_contest).first()
        if deleted_contest:
            db.session.delete(deleted_contest)
            db.session.commit()
        return redirect(url_for("my_contests_page"))
    contest = Contests.query.filter_by(id=contestid).first()
    return render_template('moreoptions.html', contest=contest,form=form,Contests=Contests,delete_form=delete_form)
codedisplay=False
@app.route("/contest/<contestid>/<page>",methods=['GET','POST'])
def contest_page(contestid,page):
    Release=ReleaseForm()
    contest=Contests.query.filter_by(id=contestid).first()
    if contest.code is None:
        released=False
    else:
        released=True

    if Release.Open.data and Release.validate():
        code=random.randint(100000,999999)
        while Contests.query.filter_by(code=str(code)).count()>0:
            code = random.randint(100000, 999999)
        contest.code=code
        db.session.commit()
        return redirect(f"/contest/{contestid}/release")
    if Release.Close.data and Release.validate():
        contest.code = None
        db.session.commit()
        return redirect(f"/contest/{contestid}/release")


    return render_template('contest.html',Results=Results,page=page,contest=contest,Release=Release,released=released,codedisplay=codedisplay)

@app.route("/join/<contestcode>",methods=["GET","POST"])
@login_required
def join_page(contestcode):
    enterform=EnterForm()
    contest=Contests.query.filter_by(code=(contestcode))
    if contest.count()==0:
        return render_template("not-found.html")
    else:
        contest=contest.first()
        if request.method=="POST":
            if Results.query.filter_by(user=current_user.id,contest=contest.id).count()!=0:
                et=Results.query.filter_by(user=current_user.id,contest=contest.id).first().endtime
                db.session.delete(Results.query.filter_by(user=current_user.id,contest=contest.id).first())
                db.session.add(Results(firstname=enterform.firstname.data, lastname=enterform.lastname.data,
                                       email=enterform.email.data, user=current_user.id, contest=contest.id,
                                       submission="", result=""
                                       , endtime=et))
            else:
                db.session.add(Results(firstname=enterform.firstname.data,lastname=enterform.lastname.data,
                                   email=enterform.email.data,user=current_user.id,contest=contest.id,submission="",result=""
                                   ,endtime=time.time()*1000+contest.time*1000+2000))
            db.session.commit()
            return redirect(f"/in/{contestcode}")
        return render_template("join.html",enterform=enterform,contest=contest)

@app.route("/join-by-code",methods=["GET","POST"])
@login_required
def join_by_code_page():
    form=CodeForm()
    if form.submit.data and form.validate():
        contest = Contests.query.filter_by(code=(form.code.data))
        if contest.count() == 0:
            flash("Invalid Code",category="danger")
        else:
            contest = contest.first()
            return redirect(f"/join/{form.code.data}")
    return render_template("join-by-code.html",form=form)

@app.route("/in/<contestcode>",methods=["GET","POST"])
@login_required
def in_page(contestcode):
    contest = Contests.query.filter_by(code=(contestcode))

    if contest.count() == 0:
        return render_template("not-found.html")
    else:
        contest=contest.first()
        result=Results.query.filter_by(user=current_user.id,contest=contest.id).first()
        form = ContestForm()
        if request.method=="GET":
            entries_data=[]
            for x in range(Questions.query.filter_by(contest=contest.id,type="Free Response Question").count()):
                entries_data.append({'answer':""})
            form.process(data={'answers':entries_data})

        if request.method=="POST":
            result.submission=""
            result.result=""
            result.score=0
            ctr=0
            for x in range(Questions.query.filter_by(contest=contest.id).count()):
                if Questions.query.filter_by(contest=contest.id,position=x).first().type=="Free Response Question":
                    result.submission+=form.answers[ctr].answer.data
                    result.submission+="#%#~"
                    if Questions.query.filter_by(contest=contest.id, position=x).first().answer==form.answers[ctr].answer.data:
                        result.result+="2#%#~"
                        result.score+=1
                    elif form.answers[ctr].answer.data=="":
                        result.result += "1#%#~"
                    else:
                        result.result += "0#%#~"
                    ctr+=1
            db.session.commit()
            print(result.submission)
            print(result.result)
            return render_template('submitted.html')
        if Results.query.filter_by(user=current_user.id,contest=contest.id).count()==0:
            return render_template("not-found.html")
        else:
            return render_template("in.html",contest=contest,Questions=Questions,form=form,result=result)
@app.route("/details/<resultid>")
def details_page(resultid):
    result=Results.query.filter_by(id=resultid).first()
    return render_template("details.html",result=result,submission=result.submission.split("#%#~"),results=result.result.split("#%#~"),
                           Contests=Contests,Questions=Questions)
