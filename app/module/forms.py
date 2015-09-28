# Import Form and RecaptchaField (optional)

from flask_wtf import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField,RadioField

# Import Form validators
from wtforms.validators import Required


# Define the login form (WTForms)

class SearchForm(Form):
      search = TextField('name', [Required(message='Enter something')])
      criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')


class AddForm(Form):
      new_author = TextField('new_author')
      new_book = TextField('new_book')

class RemoveForm(Form):
      rem_name = TextField('rem_name',[Required(message='Enter something')])
      rem_criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')
      

class EditForm(Form):
      rem_name = TextField('rem_name')
      ed_criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')