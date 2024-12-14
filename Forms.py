from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField
import shelve

class signUp(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email("Please Enter a Valid Email Address"),])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6, max = 20)])
    submit = SubmitField('Sign Up', name= 'signup_submit')
    def validate_email(self, email):
        with shelve.open('users') as usersDB:
            print(usersDB.keys())
            print("validating " , self.email.data)
            if email.data in usersDB.keys():
                raise ValidationError('Email already registered.')
                return False



class signIn(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6, max = 20)])
    submit = SubmitField('Sign In', name = 'signin_submit')

