from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from app import db

association_table = db.Table('association', db.Model.metadata,
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), onupdate="cascade"),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), onupdate="cascade")
                             )

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    a = relationship("Book", secondary=association_table, backref='posts',\
                           lazy='joined')
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '%r' % (self.name)



class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    b = relationship("Author", secondary=association_table, backref='posts',\
                           lazy='joined')


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '%r' % (self.name)



