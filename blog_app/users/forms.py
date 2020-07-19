from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import Length,EqualTo,Email,InputRequired,ValidationError
from flask_login import current_user
from blog_app.models import BlogPost,User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(min=2 ,max=20)])
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another')


class LoginForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators=[InputRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Sigin')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(min=2 ,max=20)])
    email = StringField('Email',validators=[InputRequired(), Email()])
    picture =FileField('Update profile picture',validators=[FileAllowed(['jpg','jpeg','png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account for the above user name ,Please register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(), EqualTo('password')])

    submit = SubmitField('Change Password')