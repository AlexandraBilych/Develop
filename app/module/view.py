from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db,app
import json
from app.module.forms import SearchForm, RemoveForm, AddForm, EditForm
from app.module.models import Author, Book
from sqlalchemy import func

main = Blueprint('main', __name__, url_prefix='/')
search = Blueprint('search', __name__)
remove = Blueprint('remove', __name__)
edit = Blueprint('edit', __name__)
add_author = Blueprint('add_author', __name__)
add_book = Blueprint('add_book', __name__)

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
        if checked == 'value_book' and \
        db.session.query(Book).filter(func.lower(Book.name).contains(func.lower(search_request))).all():
            list = [
                {'b_name': book.name, 'a_name': [author.name for author in book.b]}
                for book in db.session.query(Book).\
                    filter(func.lower(Book.name).contains(func.lower(search_request))).all()
                ]
            return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchBook=list,SearchForm=SearchForm(criterion='value_book'),\
                               RemoveForm=RemoveForm(),error=error)

        elif checked == 'value_author' and \
        db.session.query(Author).filter(func.lower(Author.name).contains(func.lower(search_request))).all():
            list = [
                {'a_name': author.name, 'b_name': [book.name for book in author.a]}
                for author in db.session.query(Author).\
                    filter(func.lower(Author.name).contains(func.lower(search_request))).all()
                ]
            return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchAuthor=list,\
                               SearchForm=SearchForm(criterion='value_author'),\
                               RemoveForm=RemoveForm(),error=error)
        else:
            error = 'Search by \"'+search_request+'\" didn\'t return any results'
            return redirect(url_for('main.first',error=error))

@remove.route('/remove', methods=['GET'])
def Rem():
    error = None
    checked = request.args.get('rem_criterion', '')
    search_request = request.args.get('RemoveForm.rem_name', '')
    if checked == 'value_book' and db.session.query(Book).filter(Book.name == search_request).first():
        book = db.session.query(Book).filter(Book.name == search_request).first()
        db.session.delete(book)
        db.session.commit()
        flash("'" + search_request + "' was successfully removed!")
        return redirect(url_for('main.first'))
    elif checked == 'value_author'and db.session.query(Author).filter(Author.name == search_request).first():
        author = db.session.query(Author).filter(Author.name == search_request).first()
        db.session.delete(author)
        db.session.commit()
        flash("'" + search_request + "' was successfully removed!")
        return redirect(url_for('main.first'))
    else:
        flash("Error: '" + search_request + "' isn't in the library!")
        return redirect(url_for('main.first'))

@edit.route('/edit', methods=["POST"])
def Edit():
    error = None
    if request.method == 'POST':

        checked = request.form["criterion"]
        search_request = request.form["list"]
        new_name = request.form["edit_name"]
        if checked == "value_book":
            book = db.session.query(Book).filter(Book.id == search_request).first()
            if new_name==book.name:
                return redirect(url_for('main.first'))
            else:
                book.name = new_name
                db.session.commit()
                flash("Book was succesfully renamed!")
                return redirect(url_for('main.first'))
        elif checked == 'value_author':
            author = db.session.query(Author).filter(Author.id == search_request).first()
            author.name = new_name
            db.session.commit()
            flash("Author was succesfully renamed!")
            return redirect(url_for('main.first'))
        else:
            error = "This book/author isn't in the library!"
            return redirect(url_for('main.first',error=error))

@add_author.route('/add_author', methods=["POST"])
def author():
    author_name = request.form["aadd_name"]
    book_name = request.form["book_list"]

    if not db.session.query(Author).filter(Author.name == author_name).first():
        db.session.add(Author(author_name))
        flash('New author: "' + author_name + '" was added in the library!')

    author = db.session.query(Author).filter(Author.name == author_name).first()

    if book_name is "":
        if [d for d in author.a] != []:
            author.a = []
            flash('Deleted books for author: "' + author_name + '"!')
    else:
        if not db.session.query(Book).filter(Book.name == book_name).first():
            db.session.add(Book(book_name))
            flash('New book: "' + book_name + '" was added in the library!')

        book = db.session.query(Book).filter(Book.name == book_name).first()
        author.a.append(book)
        flash('Book "' + book.name + '" was added to author "' + author_name +'"!')

    db.session.commit()
    return redirect(url_for('main.first'))


@add_book.route('/add_book', methods=["POST"])
def book():
    book_name = request.form["badd_name"]
    author_name = request.form["author_list"]

    if not db.session.query(Book).filter(Book.name == book_name).first():
        db.session.add(Book(book_name))
        flash('New book: "' + book_name + '" was added in the library!')

    book = db.session.query(Book).filter(Book.name == book_name).first()

    if author_name is "":
        if [d for d in book.b] != []:
            book.b = []
            flash('Deleted authors for book: "' + book_name + '"!')
    else:
        if not db.session.query(Author).filter(Author.name == author_name).first():
            db.session.add(Author(author_name))
            flash('New author: "' + author_name + '" was added in the library!')

        author = db.session.query(Author).filter(Author.name == author_name).first()
        book.b.append(author)
        flash('Author "' + author.name + '" was added to book "' + book_name +'"!')

    db.session.commit()
    return redirect(url_for('main.first'))


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