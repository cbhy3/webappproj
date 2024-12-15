
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField
from flask import session
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
    def validate_password(self,password):
        try:
             with shelve.open('users') as usersDB:
                  u = usersDB[self.email.data]
                 ## print(u.verifyUser(password.data))

             if u.verifyUser(password.data):
                  return True
             else:
                 raise ValidationError('Incorrect Password or Email.')
        except KeyError:
            raise ValidationError("Email doesn't exist.")


class Otp(FlaskForm):
    otp = StringField('Enter the 6 digit code sent to your email', validators=[DataRequired(),Length(min=6, max = 6)])
    submit = SubmitField('Submit', name = 'otp_submit')
    def validate_otp(self,otp):
        t = session.get('otp')
        print(t)
        if str(otp.data) == str(t):
            print("otp successfully validated")
            return True
        else:
            print(otp.data)
            raise ValidationError('Invalid OTP entered.')