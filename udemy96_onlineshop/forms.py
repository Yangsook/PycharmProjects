from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
class CreateItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    img_url = StringField("Item Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Item")

class ShowItemForm(FlaskForm):
    count = IntegerField("Count", validators=[DataRequired()])
    submit = SubmitField("Add to Cart")

class ShowCartForm(FlaskForm):
    # id = IntegerField("ID", validators=[DataRequired()])
    submit = SubmitField("Order")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    tel = StringField("Tel", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

# class CommentForm(FlaskForm):
#     comment_text = CKEditorField("Comment", validators=[DataRequired()])
#     submit = SubmitField("Submit Comment")
