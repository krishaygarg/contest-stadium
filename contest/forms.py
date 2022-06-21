from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from contest.models import User
class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self,email_address_to_check):
        email_address=User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email already exists! Please try a different email')

    username=StringField(label='Username: ',validators=[Length(min=2,max=100),DataRequired()])
    email_address=StringField(label='Email: ',validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password: ', validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username=StringField(label="Username:", validators=[DataRequired()])
    password=PasswordField(label="Password:",validators=[DataRequired()])
    submit=SubmitField(label="Sign in")

class CreateNewForm(FlaskForm):
    submit = SubmitField(label="+ Create New")

class MoreOptionsForm(FlaskForm):
    rename = StringField(label="Rename", validators=[DataRequired()])
    save = SubmitField(label="Save")

class DeleteForm(FlaskForm):
    delete=SubmitField(label="Delete")

class QuestionForm(FlaskForm):
    question=StringField(label=None, validators=[DataRequired()])
    answer = StringField(label=None)
    submit=SubmitField(label="Save")
