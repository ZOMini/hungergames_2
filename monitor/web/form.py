from flask_wtf import FlaskForm
from wtforms import fields, validators


class UrlButtonForm(FlaskForm):
    url = fields.URLField('Url', validators=[validators.URL(), ])
    submit = fields.SubmitField()


class FileButtonForm(FlaskForm):
    file = fields.FileField('File')
    submit = fields.SubmitField()


class IdFileButtonForm(FileButtonForm):
    id = fields.StringField('id_link', validators=[validators.UUID(), ])
    file = fields.FileField('File')
    submit = fields.SubmitField()
