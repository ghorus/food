from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from foods.models import User
from wtforms import BooleanField,FloatField,IntegerField,PasswordField,StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length,NumberRange, EqualTo, Email, ValidationError

class CreateGameRoomForm(FlaskForm):
    name = StringField('Title of Adlib', validators=[DataRequired()],render_kw={"placeholder": "Title of your adlib here*"})
    submit = SubmitField('Create Game')

class GameRoomMessageForm(FlaskForm):
    message = StringField('Your Adlib',validators=[DataRequired()])
    submit = SubmitField('+')

class JoinRoomForm(FlaskForm):
    member = IntegerField('Member',validators=[DataRequired()])
    room = StringField('Room ID',validators=[DataRequired()])
    submitJoin = SubmitField('Join Game')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()],render_kw={"placeholder": "example@example.com*"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder": "Your password here*"})
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    address = StringField('Store Address',render_kw={"placeholder": "Input address of store here*"})
    category = StringField('Food Category',render_kw={"placeholder": "Input food category here*"})
    content = TextAreaField('Your Thoughts?',render_kw={"placeholder": "Your review here*"})
    likes = BooleanField('Like')
    name = StringField('Store Name*', validators=[DataRequired()],render_kw={"placeholder": "Name of store here*"})
    picture = FileField('Picture of Food',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    price = FloatField('Price of Food')
    rating = IntegerField('Rate out of 5*',validators=[DataRequired(),NumberRange(max=5)])
    title = StringField('Food Item Name and/or Number*', validators=[DataRequired()],render_kw={"placeholder": "Title of your post*"})
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder": "Confirm password here*"})
    email = StringField('Email', validators=[DataRequired(),Email()],render_kw={"placeholder": "Input email here*"})
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8, max=35)],render_kw={"placeholder": "Your password here*"})
    submit = SubmitField('Sign Up')
    username = StringField('Username', validators=[DataRequired(), Length(min=5,max=20)],render_kw={"placeholder": "Create your usename here*"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already taken.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()],render_kw={"placeholder": "Input email here*"})
    submit = SubmitField('Request')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('There is no account for this email.')

class ResetPasswordForm(FlaskForm):
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8, max=35)])
    submit = SubmitField('Reset')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField('Update')
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken.')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is already taken.')
        

