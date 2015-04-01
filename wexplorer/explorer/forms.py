# -*- coding: utf-8 -*-

from flask.ext.uploads import UploadSet
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextField, PasswordField, ValidationError, BooleanField
from wtforms.validators import DataRequired

from wexplorer.extensions import bcrypt
from wexplorer.explorer.models import FileUploadPassword

class SearchBox(Form):
    q = TextField('Search', validators=[DataRequired()])
    expiring = BooleanField('Expiring Contracts')
    expired = BooleanField('Expired Contracts')

    def __init__(self, *args, **kwargs):
        super(SearchBox, self).__init__(*args, **kwargs)

class NewItemBox(Form):
    item = TextField('New Item', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(NewItemBox, self).__init__(*args, **kwargs)

class FileUpload(Form):
    upload = FileField('datafile', validators=[
        FileRequired(),
        FileAllowed(['xls', 'xlsx'], '.xls and .xlsx files only')
    ])
    password = PasswordField('Password',
                                validators=[DataRequired()])

    def validate_password(form, field):
        current_password = FileUploadPassword.query.first()
        if not bcrypt.check_password_hash(current_password.password, field.data):
            raise ValidationError('File upload password incorrect')
