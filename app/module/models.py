from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from app import db

Base = declarative_base()

association_table = db.Table('association', Base.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), onupdate="cascade"),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), onupdate="cascade")
)

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False,
                                            unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % (self.name)



class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False,
                                            unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Book %r>' % (self.name)
