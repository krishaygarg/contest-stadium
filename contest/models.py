from contest import db, login_manager
from contest import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    contests=db.relationship('Contests',backref='owned_user',lazy=True)
    @property
    def prettier_budget(self):
        if len(str(self.budget))==4:
            return f"{self.budget}"
        else:
            return f"{self.budget}"
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)


    def __repr__(self):
        return f'User {self.username}'
class Contests(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    code=db.Column(db.String())
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
    type=db.Column(db.String(),nullable=False)
    questions=db.relationship('Questions',backref='owned_contest',lazy=True)
    setup=db.Column(db.Integer())



class Questions(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    type=db.Column(db.String(),nullable=False)
    question=db.Column(db.String())
    answer=db.Column(db.String())
    contest=db.Column(db.Integer(),db.ForeignKey('contests.id'))
    setup=db.Column(db.Integer())
    position=db.Column(db.Integer(),nullable=False)


