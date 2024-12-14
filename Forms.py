from wtforms import *
from wtforms.validators import DataRequired


class createCustomer(Form):
    username = StringField('Username',validators.Length(min = 1, max = 25) ,validators=[DataRequired()])
    email = StringField('Email', validators.Length(min=1, max=320), validators=[DataRequired()])
    password = StringField('Password', validators.Length(min=1, max=20), validators=[DataRequired()])
    verifyPassword = StringField('verifyPassword', validators.Length(min=1, max=20), validators=[DataRequired()])