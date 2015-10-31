from app import db
from app.module.models import Author, Book

db.drop_all()
db.create_all()

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

