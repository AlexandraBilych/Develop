from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db
import json
from app.module.forms import SearchForm

from app.module.models import Author, Book

#db.session.add(Author('WW'))
#



# Define the blueprint: 'auth', set its url prefix: app.url/auth

main = Blueprint('main', __name__, url_prefix='/main')
search = Blueprint('search', __name__, url_prefix='/search')

# Set the route and accepted methods
@main.route('/', methods=['GET', 'POST'])
def first():
    form = SearchForm()
    a = [
     {'b_name': book.name, 'a_name': [author.name for author in book.b]}
        for book in db.session.query(Book).all()
     ]
    return render_template('show_entries.html', SearchBook=a, form=form)

@search.route('/', methods=['GET','POST'])
def find():
    checked = request.args.get('criterion', '')
    search_request =request.args.get('search', '')
    if checked == 'value_book':
        list = [
            {'b_name': book.name, 'a_name': [author.name for author in book.b]}
            for book in db.session.query(Book).\
                filter(Book.name.contains(search_request)).all()
            ]
        return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchBook=list,form=SearchForm())

    elif checked == 'value_author':
        list = [
            {'a_name': author.name, 'b_name': [book.name for book in author.a]}
            for author in db.session.query(Author).\
                filter(Author.name.contains(search_request)).all()
            ]
        return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchAuthor=list,\
                               form=SearchForm(criterion='value_author'))

