from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class SearchBox(Form):
    q = TextField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(SearchBox, self).__init__(*args, **kwargs)
