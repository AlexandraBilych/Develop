from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db,app
import json
from app.module.forms import SearchForm, RemoveForm
from app.module.models import Author, Book, association_table
from sqlalchemy import func

main = Blueprint('main', __name__, url_prefix='/')
search = Blueprint('search', __name__)
remove = Blueprint('remove', __name__)
edit = Blueprint('edit', __name__)
add_author = Blueprint('add_author', __name__)
add_book = Blueprint('add_book', __name__)

@main.route('/', methods=['GET','POST'])
def first(error=None):
    error = None
    list = [
            {'b_name': book.name, 'a_name': [author.name for author in book.b]}
            for book in db.session.query(Book).\
                   filter().all()
            ]
    return render_template('show_entries.html',\
        a=request.args.get('search', ''),\
        SearchBook=list,SearchForm=SearchForm(criterion='value_book', search=""),\
        RemoveForm=RemoveForm(),error=error)

@search.route('/search', methods=["POST"])
def find():
        error = None
        form = SearchForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            checked = request.form['criterion']
            search_request = request.form['search']
            if checked == 'value_book' and \
            db.session.query(Book).filter(func.lower(Book.name).contains(func.lower(search_request))).all():
                list = [
                    {'b_name': book.name, 'a_name': [author.name for author in book.b]}
                    for book in db.session.query(Book).\
                        filter(func.lower(Book.name).contains(func.lower(search_request))).all()
                    ]
                return render_template('show_entries.html',\
                                   a=request.args.get('search', ''),\
                                   SearchBook=list,SearchForm=SearchForm(criterion='value_book', search=search_request),\
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
                                   SearchForm=SearchForm(criterion='value_author', search=search_request),\
                                   RemoveForm=RemoveForm(),error=error)
            else:
                error = 'Search by \"'+search_request+'\" didn\'t return any results'
                return redirect(url_for('main.first',error=error))


@remove.route('/remove', methods=["POST"])
def Rem():
    form = RemoveForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        checked = request.form['rem_criterion']
        search_request = request.form['rem_name']
        if checked == 'value_book' and db.session.query(Book).filter(func.lower(Book.name) == func.lower(search_request)).first():
            book = db.session.query(Book).filter(func.lower(Book.name) == func.lower(search_request)).first()
            db.session.delete(book)
            db.session.commit()
            flash("'" + book.name + "' was successfully removed!")
            return redirect(url_for('main.first'))
        elif checked == 'value_author'and db.session.query(Author).filter(func.lower(Author.name) == func.lower(search_request)).first():
            author = db.session.query(Author).filter(func.lower(Author.name) == func.lower(search_request)).first()
            db.session.delete(author)
            db.session.commit()
            flash("'" + author.name + "' was successfully removed!")
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
        List = request.form.getlist("first")
		
        if checked == 'value_book':
            book = db.session.query(Book).filter(Book.id == search_request).first()
            if new_name != book.name:
                book.name = new_name
                db.session.commit()
                flash("Book was succesfully renamed!")
            authors = db.session.query(Book).filter(func.lower(Book.name) == func.lower(new_name)).first().b
            for author in authors:
                if author.name not in List:
                    au = db.session.query(Author).filter(Author.name == author.name).first()
                    book.b.remove(au)
                    db.session.commit()
                    flash("You ripped \"" + book.name + "\" and \"" + author.name +"\"!")
            else:
                return redirect(url_for('main.first'))
        elif checked == 'value_author':
            author = db.session.query(Author).filter(Author.id == search_request).first()
            if new_name != author.name:
                author.name = new_name
                db.session.commit()
                flash("Author was succesfully renamed!")
            books = db.session.query(Author).filter(func.lower(Author.name) == func.lower(new_name)).first().a
            for book in books:
                if book.name not in List:
                    bo = db.session.query(Book).filter(Book.name == book.name).one()
                    author.a.remove(bo)
                    db.session.commit()
                    flash("You ripped \"" + book.name + "\" and \"" + author.name +"\"!")
        else:
            error = "This book/author isn't in the library!"
            return redirect(url_for('main.first',error=error))
    return redirect(url_for('main.first'))

@add_author.route('/add_author', methods=["POST"])
def author():
    author_name = request.form["aadd_name"]
    book_name = request.form["book_list"]

    if not db.session.query(Author).filter(func.lower(Author.name) == func.lower(author_name)).first():
        db.session.add(Author(author_name))
        db.session.commit()
        flash('New author: "' + author_name + '" was added in the library!')

    author = db.session.query(Author).filter(func.lower(Author.name) == func.lower(author_name)).first()

    if book_name is "":
        pass
    else:
        if not db.session.query(Book).filter(func.lower(Book.name) == func.lower(book_name)).first():
            db.session.add(Book(book_name))
            db.session.commit()
            flash('New book: "' + book_name + '" was added in the library!')

        book = db.session.query(Book).filter(func.lower(Book.name) == func.lower(book_name)).first()
        author.a.append(book)
        flash('Book "' + book.name + '" was added to author "' + author_name +'"!')

    db.session.commit()
    return redirect(url_for('main.first'))


@add_book.route('/add_book', methods=["POST"])
def book():
    book_name = request.form["badd_name"]
    author_name = request.form["author_list"]

    if not db.session.query(Book).filter(func.lower(Book.name) == func.lower(book_name)).first():
        db.session.add(Book(book_name))
        db.session.commit()
        flash('New book: "' + book_name + '" was added in the library!')

    book = db.session.query(Book).filter(func.lower(Book.name) == (book_name)).first()

    if author_name is "":
        pass
    else:
        if not db.session.query(Author).filter(func.lower(Author.name) == func.lower(author_name)).first():
            db.session.add(Author(author_name))
            db.session.commit()
            flash('New author: "' + author_name + '" was added in the library!')

        author = db.session.query(Author).filter(func.lower(Author.name) == func.lower(author_name)).first()
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

@app.route('/GetAutorsforBook', methods=['GET','POST'])
def GetAutorsforBook():
    if request.method == 'POST':
        dict = request.get_json('edit_name')
        for i in dict.values():
            name = i
        book = db.session.query(Book).filter(func.lower(Book.name).contains(func.lower(name))).one()
        if book.b:
            return json.dumps([
                {'name': [author.name for author in db.session.query(Book).\
                filter(func.lower(Book.name).contains(func.lower(name))).one().b]}
            ])

@app.route('/GetBooksforAuthor', methods=['GET','POST'])
def GetBooksforAuthor():
    if request.method == 'POST':
        dict = request.get_json('edit_name')
        for i in dict.values():
            name = i
        author = db.session.query(Author).filter(func.lower(Author.name).contains(func.lower(name))).one()
        if author.a:
            return json.dumps([
                {'name': [book.name for book in db.session.query(Author).\
                filter(func.lower(Author.name).contains(func.lower(name))).one().a]}
            ])

@app.route('/GetAuthorList', methods=['POST'])
def GetAuthorList():
    authors = db.session.query(Author).all()
    return json.dumps([
        {'id': author.id, 'name': author.name}
        for author in authors
    ])
