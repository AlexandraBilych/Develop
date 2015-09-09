from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db
import json
from app.module.forms import SearchForm

from app.module.models import Author, Book

#db.session.add(Author('WW'))
#



# Define the blueprint: 'auth', set its url prefix: app.url/auth

search = Blueprint('search', __name__, url_prefix='/search')
# Set the route and accepted methods
@search.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = SearchForm()
    query = db.session.query(Author).all()
    a = json.dumps([
    ( author.name, [book.name for book in author.b])
        for author in db.session.query(Author).all()
    ])
    query1 = db.session.query(Book).all()
    return render_template('show_entries.html', a=query, Books=query1, form=form)