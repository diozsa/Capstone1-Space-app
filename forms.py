from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    """User form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

# class DeleteForm(FlaskForm):
#     """Delete form. This form is blank."""

class SearchForm(FlaskForm):
    """Search form for image search"""
    search = StringField("Search", validators=[InputRequired()])
