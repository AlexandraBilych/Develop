from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db
from app.module.forms import SearchForm

from app.module.models import Author, Book

#db.session.add(Author('WW'))
#

#db.session.add(Author(name='sss'))
#db.session.add(Author(name='eee'))
#db.session.commit()
for row in db.session.query(Author).all():
    print(row.id, row.name, 'rrr')
#db.session.commit()
# Define the blueprint: 'auth', set its url prefix: app.url/auth

search = Blueprint('search', __name__, url_prefix='/search')
# Set the route and accepted methods
@search.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = SearchForm()
    Authors = [dict(id=row.id,name=row.name) for row in db.session.query(Author).all()]
    print("Value : %s" %  Authors.items())
    Books = [dict(id=row[0],name=row[1]) for row in Book.query.all()]
    return render_template('show_entries.html', Authors=Authors, Books=Books, form=form)