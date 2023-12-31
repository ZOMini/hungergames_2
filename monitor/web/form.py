import uuid

from flask_wtf import FlaskForm
from wtforms import fields, validators


class UrlButtonForm(FlaskForm):
    url = fields.URLField('Url', validators=[validators.URL(), validators.DataRequired()])
    submit = fields.SubmitField()


class FileButtonForm(FlaskForm):
    file = fields.FileField('File', validators=[validators.DataRequired()])
    submit = fields.SubmitField()


class IdFileButtonForm(FlaskForm):
    id = fields.StringField('Id', validators=[validators.DataRequired()])
    file = fields.FileField('File', validators=[validators.DataRequired()])
    submit = fields.SubmitField()

    def validate_id(form, field):
        try:
            uuid.UUID(field.data)
        except Exception:
            raise ValueError('Invalid UUID.')


class LinksFilterForm(FlaskForm):
    available = fields.SelectField('Available', choices=[('all', 'All'), ('True', 'True'), ('False', 'False')])
    domain = fields.StringField('Domain name')
    suffix = fields.StringField('Domain zone')
    submit = fields.SubmitField('Filter')


class SignupForm(FlaskForm):
    name = fields.StringField('Name', validators=[validators.DataRequired()])
    email = fields.EmailField('Email', validators=[validators.DataRequired()])
    password = fields.PasswordField('Password', validators=[validators.DataRequired()])
    confirm = fields.PasswordField('Confirm', validators=[validators.DataRequired()])
    submit = fields.SubmitField('Submit')
