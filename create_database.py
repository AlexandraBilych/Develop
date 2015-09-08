from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

Base = declarative_base()

engine = create_engine("sqlite:///app.db")

session = Session(engine)
connection = session.connection()
connection.execute( """ pragma foreign_keys=on """ )
 
session.add(author('Sasha'))
#session.add(Author(id=2,name='Ivan'))
#session.add(Book(name='single'))
#session.add(Book(id=12,name='multi'))
#session.add(Library(author_id=1, book_id=2))
 
#session.query(db.Book).filter_by(dname='B').update({"id":20})
 
session.commit()
session.close()
 

#print(Search(Author))
for row in Base.metadata.sorted_tables:
    print(row)
 
#for data in session.query(Library).all():
#     print(data.id, data.author_id, data.book_id)
 
#for data in session.query(Author).all(): 
#     print(data.id, data.name)
      
#for data in session.query(Book).all():
#     print(data.id, data.name)
 
      
