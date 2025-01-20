
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField
from flask import session
import shelve
from Product import Product
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
    email = EmailField('Email', validators=[Email("Please Enter a Valid Email Address"), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max = 20)])
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
    otp = StringField('Enter the 6 digit code sent to your email', validators=[Length(min=6, max = 6), DataRequired()], )
    submit = SubmitField('Submit', name = 'otp_submit')
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

class deleteAccount(FlaskForm):
    password = PasswordField('Enter your password to confirm its you',
                             validators=[InputRequired(), Length(min=6, max=20)])
    delete = SubmitField('Delete Account', name='delete_submit')
    cancel = SubmitField('Cancel', name='delete_cancel_submit')
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

class changeEmail(FlaskForm):
    password = PasswordField('Enter your password to confirm its you', validators=[InputRequired(),Length(min=6, max = 20)])
    email = EmailField('Enter your new email', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    submit = SubmitField('Send One-Time Password to your new email', name = 'change_email_submit')
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


class changePassword(FlaskForm):
    oldPassword = PasswordField('Enter your old password', validators=[InputRequired(),Length(min=6, max = 20)])
    newPassword = PasswordField('Enter your new password', validators=[InputRequired(),Length(min=6, max = 20)])
    verifyPassword = PasswordField('Re-enter your new password', validators=[InputRequired(),Length(min=6, max = 20), EqualTo('newPassword','Passwords do not match.')])
    submit = SubmitField('Submit', name = 'change_password_submit')
    def validate_oldPassword(self,oldPassword):
        with shelve.open('users') as usersDB:
            u = usersDB[session.get('current_user')]

            if u.verifyUser(oldPassword.data):
                return True
            else:
                raise ValidationError('Incorrect Password')
    def validate_newPassword(self,newPassword):
        with shelve.open('users') as usersDB:
            u = usersDB[session.get('current_user')]
            if User.comparePassword(newPassword.data, u.password):
                raise ValidationError('New password has to be different than your old one.')
            else:
                print("new password validated")
                return True

class addProduct(FlaskForm):
    name = StringField('Enter the product\'s name', validators=[InputRequired()])
    price = FloatField('Enter the product\'s price', validators=[InputRequired()])
    quantity = IntegerField('Enter the product\'s quantity', validators=[InputRequired()])
    categories = SelectMultipleField('Select the product\'s categories', choices=tuple((cat, cat) for cat in Product.valid_categories))
    image_url = StringField('Enter the product\'s image url', validators=[DataRequired()])
    description = StringField('Enter the product\'s description', validators=[DataRequired()])
    expiry = DateField('Enter the product\'s expiry date',validators=[InputRequired()])
    weight = IntegerField('Enter the product\'s weight', validators=[InputRequired()])
    submit = SubmitField('Submit', name = 'add_product_submit')


class modifyProduct(FlaskForm):
    product = SelectField('Select the product to modify', validators = [InputRequired()])
    change = SelectField('What do you want to change', choices = [('name','Name'),('quantity', 'Quantity'), ('expiry', 'Expiry Date'), ('weight', 'Weight'), ('price', 'Price'), ('description', 'Description'), ('imageURL', 'Image URL'), ('categories', 'Categories')])
    name = StringField('Enter the product\'s new name')
    quantity = IntegerField('Enter the change in product\'s quantity (Enter a negative value to remove quantity)')
    expiry = DateField('Enter the product\'s new expiry date')
    weight = IntegerField('Enter the product\'s new weight')
    price = FloatField('Enter the product\'s new price')
    description = StringField('Enter the product\'s new description')
    image_url = StringField('Enter the product\'s new image url')
    categories = SelectMultipleField('Select the product\'s new categories')
    submit = SubmitField('Submit', name = 'modify_product_submit')
    delete_submit = SubmitField('Delete Product', name = "delete_submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with shelve.open('products') as products:
            self.product.choices = [
                (prod, f'{prod} ID: {products[prod].name}, Expiry: {products[prod].expiry}')
                for prod in products
            ]
        self.categories.choices = [(cat, cat) for cat in Product.valid_categories]