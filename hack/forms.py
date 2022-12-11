from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField, DateField
from wtforms.validators import DataRequired,Email,EqualTo, ValidationError,Length

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")



