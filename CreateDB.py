import json
from config import SQLALCHEMY_DATABASE_URI
from app import db
from app.module.models import Author, Book


#db.create_all()



#print([book.name for book in author.b])

#for row in db.session.query(Book.name.label('books'), Author.name).join(Author)\
#            .options(joinedload(Author.b)).all():
#    print(row.Author.name, row.Book.name)

#c = Book('three')
#v = Book('four')
#s = Author('Viva')


#s.b.append(c)
#s.b.append(v)
#db.session.add(c)
#db.session.add(v)
#db.session.commit()

#'books': [book.name for book in author.books]


#for row in Author.query.join(Book).all():
#    print(row.name)


a = json.dumps([
    ( author.name, [book.name for book in author.b])
        for author in db.session.query(Author).all()
    ])



print(a)

for row in db.session.query(Book).all():
    print(row.id, row.name)

for row in db.session.query(Author).all():
     print(row.id, row.name)


row = db.session.query(Author).all()
print(row)

