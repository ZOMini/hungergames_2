import logging
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


