from flask.ext.wtf import Form
from wtforms.fields import TextField, RadioField
from wtforms.validators import Required


class SearchForm(Form):
      search = TextField('search', validators = [Required()])
      criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')

class RemoveForm(Form):
      rem_name = TextField('rem_name', validators = [Required()])
      rem_criterion = RadioField('Label',\
                             choices=[('value_book', 'book'),\
                                      ('value_author', 'autor')],\
              default='value_book')
