from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
import phonenumbers
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError,TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from managment.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse("+91"+phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    deadline = DateField('Deadline',validators=[DataRequired()])
    project_file = FileField('project file', validators=[DataRequired(),FileAllowed(['txt', 'pdf'])])
    submit = SubmitField('ADD PROJECT')

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    deadline = DateField('Deadline',validators=[DataRequired()])
    task_file = FileField('task file', validators=[DataRequired(),FileAllowed(['txt', 'pdf'])])
    submit = SubmitField('ADD Task')

class TeamForm(FlaskForm):
   email = StringField('Email',validators=[DataRequired(), Email()])
   submit = SubmitField('ADD')