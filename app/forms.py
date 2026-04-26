from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ViolationForm(FlaskForm):
    vehicle_number = StringField('Vehicle Number', validators=[DataRequired(), Length(max=20)])
    violation_type = StringField('Violation Type', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    fine_amount = FloatField('Fine Amount', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], validators=[DataRequired()])
    submit = SubmitField('Submit')
