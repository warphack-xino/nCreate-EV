from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class CarForm(FlaskForm):
    colors =  SelectField('Colors', choices=[('Red'), ('Green'), ('Black')], validators=[DataRequired()])
    models = SelectField('Models', choices=[('v1'), ('v2'), ('v3')], validators=[DataRequired()])
    submit = SubmitField("Confirm selection")