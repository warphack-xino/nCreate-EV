from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class CarForm(FlaskForm):
    colors =  SelectField('Colors', choices=[('Red'), ('Green'), ('Black')], validators=[DataRequired()])
    models = SelectField('Models', choices=[('1', 'v1'), ('2', 'v2'), ('3', 'v3')], validators=[DataRequired()])
    submit = SubmitField("Confirm selection")