from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostTopicForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(1, 64)])
    body = TextAreaField('body', validators=[DataRequired()])
    node = StringField('node', validators=[DataRequired()])
    submit = SubmitField('submit')


class CommentForm(Form):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('submit')


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
