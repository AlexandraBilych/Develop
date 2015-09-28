import json
from config import SQLALCHEMY_DATABASE_URI
from app import db
from app.module.models import Author, Book

db.drop_all()
db.create_all()





#for row in db.session.query(Book.name.label('books'), Author.name).join(Author)\
#            .options(joinedload(Author.b)).all():
#    print(row.Author.name, row.Book.name)

b = Book('The Wheel of Time')
a1 = Author('Barbara Park')
a2 = Author('Robert Jordan')
db.session.add(b)
b.b.append(a1)
b.b.append(a2)
db.session.add(a1)
db.session.add(a2)
db.session.commit()

a = Author('J. K. Rowling')
b1 = Book('Harry Potter and the Chamber of Secrets')
b2 = Book('Harry Potter and the Prisoner of Azkaban')
b3 = Book('Harry Potter and the Goblet of Fire')
db.session.add(a)
a.a.append(b1)
a.a.append(b2)
a.a.append(b3)
db.session.add(b1)
db.session.add(b2)
db.session.add(b3)
db.session.commit()

b = Book('The Alchemist')
a = Author('Paulo Coelho')
db.session.add(b)
b.b.append(a)
db.session.add(a)
db.session.commit()

b = Book('Lolita')
a = Author('Vladimir Nabokov')
db.session.add(b)
b.b.append(a)
db.session.add(a)
db.session.commit()


#for row in Author.query.join(Book).all():
#    print(row.name)


a = [
     {'b_name' : book.name,'a_name' : [author for author in book.b ]}
        for book in db.session.query(Book).all()
    ]

print(a)

row = db.session.query(Author).all()
print(row)

for row in db.session.query(Book).all():
    print(row.id, row.name)

#book = db.session.query(Book).filter(Book.name == 'Lolita').first()
#print(book)
#db.session.delete(book)
#db.session.commit()

for row in db.session.query(Book).all():
    print(row.id, row.name)

#for row in db.session.query(Book).options(joinedload('Book.b')).all():
#     print(row.id, row.name)


row = db.session.query(Author).all()
print(row)

