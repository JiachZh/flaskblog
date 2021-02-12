from flask import flash
from flask_wtf import FlaskForm
from blog.models import Users
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, ValidationError, Regexp


class RegistrationForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^(?=.*\d).{8,15}$', message='Your password should be between 8 and 15 characters long, and contains at least one numeric digit.'), validators.EqualTo('password2', message='Passwords must match')]) 
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(userName=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please choose a different one.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            flash('User not exist or password wrong.')
        
class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post comment')