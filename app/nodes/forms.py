from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateNodeForm(Form):
    node = StringField('create node', validators=[DataRequired()])
    submit = SubmitField('submit')
