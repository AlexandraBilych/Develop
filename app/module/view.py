from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db,app
import json
from app.module.forms import SearchForm, RemoveForm, AddForm, EditForm
from app.module.models import Author, Book

main = Blueprint('main', __name__, url_prefix='/main')
search = Blueprint('search', __name__)
remove = Blueprint('remove', __name__, url_prefix='/remove')
edit = Blueprint('edit', __name__)

@main.route('/', methods=['GET','POST'])
def first(error=None):
    return render_template('show_entries.html', \
                           SearchForm=SearchForm(),\
                           RemoveForm=RemoveForm(),\
                           error=request.args.get('error', ''))

@search.route('/search', methods=['GET'])
def find():
        error = None
        checked = request.args.get('criterion', '')
        search_request =request.args.get('SearchFrom.search', '')
        if checked == 'value_book'\
                and \
                db.session.query(Book).\
                        filter(Book.name.contains(search_request)).all():
            list = [
                {'b_name': book.name, 'a_name': [author.name for author in book.b]}
                for book in db.session.query(Book).\
                    filter(Book.name.contains(search_request)).all()
                ]
            return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchBook=list,SearchForm=SearchForm(criterion='value_book'),\
                                   RemoveForm=RemoveForm(),error=error)
        elif checked == 'value_author'\
                and\
                db.session.query(Author).\
                filter(Author.name.contains(search_request)).all():
            list = [
                {'a_name': author.name, 'b_name': [book.name for book in author.a]}
                for author in db.session.query(Author).\
                    filter(Author.name.contains(search_request)).all()
                ]
            return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchAuthor=list,\
                               SearchForm=SearchForm(criterion='value_author'),\
                                   RemoveForm=RemoveForm(),error=error)
        else:
            error = 'Search by \"'+search_request+'\" didn\'t return any results'
            return redirect(url_for('main.first',error=error))

@remove.route('/', methods=['GET'])
def Rem():
    error = None
    checked = request.args.get('rem_criterion', '')
    print(checked)
    search_request = request.args.get('RemoveForm.rem_name', '')
    print(search_request)
    if checked == 'value_book' and db.session.query(Book).filter(Book.name == search_request).first():
        book = db.session.query(Book).filter(Book.name == search_request).first()
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('main.first'))
    elif checked == 'value_author'and db.session.query(Author).filter(Author.name == search_request).first():
        author = db.session.query(Author).filter(Author.name == search_request).first()
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('main.first'))
    else:
        error = "This book/author isn't in the library!"
        return redirect(url_for('main.first',error=error))

@edit.route('/edit', methods=["POST"])
def Edit():
    error = None
    print("Yes")
    print(request.method)
    if request.method == 'POST':

        checked = request.form["criterion"]
        print(checked)
        search_request = request.form["list"]
        print(search_request)
        new_name = request.form["edit_name"]
        print(new_name)
        if checked == "value_book":
            book = db.session.query(Book).filter(Book.id == search_request).first()
            if new_name==book.name:
                print('flash')
                flash("The name isn't changed")
                return redirect(url_for('main.first'))
            else:
                print('edit')
                book.name = new_name
                db.session.commit()
                flash("2The name isn't changed")
                return redirect(url_for('main.first'))
        elif checked == 'value_author':
            author = db.session.query(Author).filter(Author.id == search_request).first()
            author.name = new_name
            db.session.commit()
            return redirect(url_for('main.first'))
        else:
            error = "This book/author isn't in the library!"
            return redirect(url_for('main.first',error=error))


@app.route('/GetBookList', methods=['POST'])
def GetBookList():
    books = db.session.query(Book).all()

    return json.dumps([
        {'id': book.id, 'name': book.name}
        for book in books
    ])

@app.route('/GetAuthorList', methods=['POST'])
def GetAuthorList():
    authors = db.session.query(Author).all()

    return json.dumps([
        {'id': author.id, 'name': author.name}
        for author in authors
    ])