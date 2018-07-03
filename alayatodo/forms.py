from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(1, 20)])
    password = StringField(
        'password', validators=[DataRequired(), Length(1, 64)])


class TodoForm(FlaskForm):
    description = StringField(
        'description', validators=[DataRequired(), Length(1, 255)])
    completed = BooleanField('completed', default=False)