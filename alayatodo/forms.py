from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(1, 255)])
    password = StringField('password',
                           validators=[DataRequired(), Length(1, 255)])


class TodoForm(FlaskForm):
    description = StringField('description', validators=[Length(1, 255)])
