from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=2, max=15)])
    submit = SubmitField('Sign Up')
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])

class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
