from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from wtforms.fields import EmailField, PasswordField


def validate_password(password, confirm_password):
    if password.data != confirm_password.data:
        raise ValidationError('Passwords must match!')


class signUp(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6, max = 20)])
    submit = SubmitField('Sign Up')

class signIn(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email("Please Enter a Valid Email Address")])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=6, max = 20)])
    submit = SubmitField('Sign In')

