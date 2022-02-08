from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    _id = HiddenField('_id')
    # author = StringField('author')
    start = DateField('start', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateField('end', format='%Y-%m-%d', validators=[DataRequired()])
    subject = StringField('subject', validators=[DataRequired()])
    description = StringField('description')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
                        