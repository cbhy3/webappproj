
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField
from flask import session
import shelve
from user import User
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
    email = EmailField('Email', validators=[Email("Please Enter a Valid Email Address")])
    password = PasswordField('Password', validators=[Length(min=6, max = 20)])
    forgotpassword = SubmitField('Forgot Password', name = 'forgotpass_submit')
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
    otp = StringField('Enter the 6 digit code sent to your email', validators=[Length(min=6, max = 6)])
    submit = SubmitField('Submit', name = 'otp_submit')
    newEmail = SubmitField('Use a different Email Address.', name = 'new_email_submit')
    def validate_otp(self,otp):
        t = session.get('otp')
        print(t)
        if str(otp.data) == str(t):
            print("otp successfully validated")
            session.pop('otp')
            return True
        else:
            print(otp.data)
            raise ValidationError('Invalid OTP entered.')
class resetPasswordEmail(FlaskForm):
    email = EmailField('Enter the email of your account', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    submit = SubmitField('Reset Password', name = 'reset_password_email_submit')
    def validate_email(self,email):
        with shelve.open('users') as usersDB:
            if email.data in usersDB.keys():
                return True
            else:
                raise ValidationError('Email doesn\'t exist.')
class resetPasswordOTP(FlaskForm):
    otp = StringField("Enter the 6 digit code sent to your email to verify it's really you", validators=[Length(min=6, max = 6)])
    submit = SubmitField('Submit', name = 'resetpasswordotp_submit')
    def validate_otp(self,otp):
        t = session.get('resetotp')
        if str(otp.data) == str(t):
            print("reset otp successfully validated")
            session.pop('resetotp')
            return True
        else:
            print(otp.data)
            raise ValidationError('Invalid OTP entered.')


class resetPassword(FlaskForm):
    password = PasswordField('Enter a new password', validators=[InputRequired(),Length(min=6, max = 20)])
    verifypassword = PasswordField('Re-enter your password', validators=[InputRequired(), EqualTo('password','Passwords do not match.')])
    submit = SubmitField('Submit', name = 'reset_password_submit')
    def validate_password(self,password):
        old = session.get('oldPassword')
        if User.comparePassword(password.data, old):
            print("old password is same as new password")
            raise ValidationError('New password has to be different than your old one.')
        else:
            print("valid new password")
            session.pop('oldPassword')
            return True


class signOut(FlaskForm):
    signout = SubmitField('Sign Out', name = 'signout_submit')
    cancel = SubmitField('Cancel', name = 'signout_cancel_submit')

class changeEmail(FlaskForm):
    password = PasswordField('Enter your password to confirm its you', validators=[InputRequired(),Length(min=6, max = 20)])
    email = EmailField('Enter your new email', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    submit = SubmitField('Submit', name = 'change_email_submit')
    def validate_password(self,password):
        try:
             with shelve.open('users') as usersDB:
                  u = usersDB[session.get('current_user')]
                 ## print(u.verifyUser(password.data))

             if u.verifyUser(password.data):
                  return True
             else:
                 raise ValidationError('Incorrect Password')
        except KeyError:
            raise ValidationError("Something went wrong.")

