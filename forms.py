from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired

class BaseUserForm(FlaskForm):
    username = StringField('Username', id='uname', validators=[DataRequired()])
    password = PasswordField('Password', id='pword', validators=[DataRequired()])
    two_factor = StringField('2fa', id='2fa')


class LoginForm(BaseUserForm):
    submit = SubmitField('Login')


class RegisterForm(BaseUserForm):
    submit = SubmitField('Register')


class SpellCheckForm(FlaskForm):
    inputarea = StringField('input')
    submit = SubmitField('spell check')