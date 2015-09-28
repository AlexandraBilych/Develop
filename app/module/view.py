from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db,app
import json
from app.module.forms import SearchForm, RemoveForm, AddForm, EditForm

from app.module.models import Author, Book

#db.session.add(Author('WW'))
#



# Define the blueprint: 'auth', set its url prefix: app.url/auth

main = Blueprint('main', __name__, url_prefix='/main')
search = Blueprint('search', __name__, url_prefix='/search')
remove = Blueprint('remove', __name__, url_prefix='/remove')
datalistbook = Blueprint('datalistbook', __name__, url_prefix='/datalistbook')

# Set the route and accepted methods
@main.route('/', methods=['GET', 'POST'])
def first():
    form = SearchForm()
    a = [
     {'b_name': book.name, 'a_name': [author.name for author in book.b]}
        for book in db.session.query(Book).all()
     ]
    return render_template('show_entries.html', \
                           SearchBook=a,\
                           SearchForm=form,\
                           RemoveForm=RemoveForm(),\
                           data=json.dumps([
        {'id': book.id, 'name': book.name} \
        for book in db.session.query(Book).all()]))

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
                               SearchBook=list,SearchForm=SearchForm(),RemoveForm=RemoveForm())

    elif checked == 'value_author':
        list = [
            {'a_name': author.name, 'b_name': [book.name for book in author.a]}
            for author in db.session.query(Author).\
                filter(Author.name.contains(search_request)).all()
            ]
        return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchAuthor=list,\
                               SearchForm=SearchForm(criterion='value_author'),RemoveForm=RemoveForm())


@remove.route('/', methods=['GET','POST'])
def Rem():
    checked = request.args.get('rem_criterion', '')
    search_request = request.args.get('rem_name', '')
    print(search_request)
    if checked == 'value_book':
        book = db.session.query(Book).filter(Book.name == search_request).first()
        print(book)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('main.first'))
    elif checked == 'value_author':
        author = db.session.query(Author).filter(Author.name == search_request).first()
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('main.first'))


@datalistbook.route('/datalist_book', methods=['POST'])
def databook():
    return json.dumps([
        {'id': book.id, 'name': book.name} \
        for book in db.session.query(Book).all()])
