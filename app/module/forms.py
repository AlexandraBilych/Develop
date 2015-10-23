from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField,RadioField, validators



class SearchForm(Form):
      search = TextField('name',validators=
                             [validators.Required("Please enter name."),
                              validators.Length(min=20)])
      criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')

class AddForm(Form):
      new_author = TextField('new_author')
      new_book = TextField('new_book')

class RemoveForm(Form):
      rem_name = TextField('rem_name',validators=
                             [validators.Required("Please enter name."),
                              validators.Length(min=20)])
      rem_criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')
      

class EditForm(Form):
      edit_name = TextField('edit_name')
      ed_criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')