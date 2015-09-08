# Import Form and RecaptchaField (optional)

from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField

# Import Form validators
from wtforms.validators import Required


# Define the login form (WTForms)

class SearchForm(Form):
      search  = TextField('name', [Required(message='Enter something')])