from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db,app
import json
from app.module.forms import SearchForm, RemoveForm, AddForm, EditForm
from app.module.models import Author, Book

main = Blueprint('main', __name__, url_prefix='/')
search = Blueprint('search', __name__)
remove = Blueprint('remove', __name__, url_prefix='/remove')
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
        db.session.query(Book).filter(Book.name.contains(search_request)).all():
            list = [
                {'b_name': book.name, 'a_name': [author.name for author in book.b]}
                for book in db.session.query(Book).\
                    filter(Book.name.contains(search_request)).all()
                ]
            return render_template('show_entries.html',\
                               a=request.args.get('search', ''),\
                               SearchBook=list,SearchForm=SearchForm(criterion='value_book'),\
                               RemoveForm=RemoveForm(),error=error)

        elif checked == 'value_author' and \
        db.session.query(Author).filter(Author.name.contains(search_request)).all():
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
    search_request = request.args.get('RemoveForm.rem_name', '')
    if checked == 'value_book' and db.session.query(Book).filter(Book.name == search_request).first():
        book = db.session.query(Book).filter(Book.name == search_request).first()
        db.session.delete(book)
        db.session.commit()
        flash("Book was successfully removed!")
        return redirect(url_for('main.first'))
    elif checked == 'value_author'and db.session.query(Author).filter(Author.name == search_request).first():
        author = db.session.query(Author).filter(Author.name == search_request).first()
        db.session.delete(author)
        db.session.commit()
        flash("Author was successfully removed!")
        return redirect(url_for('main.first'))
    else:
        flash("This book/author isn't in the library!")
        return redirect(url_for('main.first'))

@edit.route('/edit', methods=["POST"])
def Edit():
    error = None
    print("Yes")
    print(request.method)
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
                return redirect(url_for('main.first'))
        elif checked == 'value_author':
            author = db.session.query(Author).filter(Author.id == search_request).first()
            author.name = new_name
            db.session.commit()
            return redirect(url_for('main.first'))
        else:
            error = "This book/author isn't in the library!"
            return redirect(url_for('main.first',error=error))

@add_author.route('/add_author', methods=["POST"])
def author():
    author_name = request.form["aadd_name"]
    book_id = request.form["book_list"]
    if not db.session.query(Author).filter(Author.name == author_name).first():
        db.session.add(Author(author_name))
        db.session.commit()
        flash(author_name)

    if db.session.query(Book).filter(Book.id == book_id).first():
        book = db.session.query(Book).filter(Book.id == book_id).first()
        author = db.session.query(Author).filter(Author.name == author_name).first()
        author.a.append(book)
        db.session.commit()
        flash(book_id)
    return redirect(url_for('main.first'))

@add_book.route('/add_book', methods=["POST"])
def book():
    book_name = request.form["badd_name"]
    author_id = request.form["author_list"]
    if not db.session.query(Book).filter(Book.name == book_name).first():
        db.session.add(Book(book_name))
        db.session.commit()
        flash(book_name)

    if db.session.query(Author).filter(Author.id == author_id).first():
        author = db.session.query(Author).filter(Author.id == author_id).first()
        book = db.session.query(Book).filter(Book.name == book_name).first()
        book.b.append(author)
        db.session.commit()
        flash(author_id)
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