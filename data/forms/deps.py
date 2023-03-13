from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo


class DepsForm(FlaskForm):
    title = StringField('Title of Department', validators=[DataRequired()])
    chief = StringField('Chief Id', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Department email', validators=[DataRequired()])
    submit = SubmitField('Submit')
