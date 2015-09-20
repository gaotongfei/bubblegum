from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import (DataRequired, Length, Email, URL,
                                EqualTo, Regexp)


class SignupForm(Form):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('username', validators=[
        DataRequired(), Length(1, 16), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'username must have only letters,'
                                              'numbers, dots or undersocres')])
    password = PasswordField('password', validators=[
        DataRequired(), Length(1, 16),
        EqualTo('retype_password', message='password dont match')])
    retype_password = PasswordField('retype', validators=[DataRequired()])
    submit = SubmitField('signup')


class LoginForm(Form):
    username = StringField('username',
                           validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('password',
                             validators=[DataRequired(), Length(1, 16)])
    remember_me = BooleanField('remember me')
    submit = SubmitField('login')


class ProfileForm(Form):
    username = StringField('username')
    email = StringField('email')
    website = StringField('website', validators=[URL()])
    bio = StringField('bio')
    submit = SubmitField('submit')


class AccountForm(Form):
    email = StringField('email', validators=[DataRequired(), Length(1, 64)])
    current_password = PasswordField('current password', validators=[DataRequired(), Length(1, 16)])
    new_password = PasswordField('new password', validators=[
        DataRequired(), Length(1, 16),
        EqualTo('retype_password', message='password dont match')])
    retype_password = PasswordField('retype', validators=[DataRequired()])
    submit = SubmitField('submit')
