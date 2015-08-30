#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# A library that provides accessing the database
import sqlite3
import csv

''' Create three databases: Author, Book, Library '''
source = sqlite3.connect('sourse.db')

cur = source.cursor()

#Author
cur.execute("""
    CREATE TABLE AUTHOR
        (AUTHOR_ID INTEGER PRIMARY KEY,
         AUTHOR_NAME TEXT) """)

with open('AUTHOR.csv','r') as lines:
    line = csv.DictReader(lines)
    in_db = [(i['AUTHOR_ID'], i['AUTHOR_NAME']) for i in line]

cur.executemany("INSERT INTO AUTHOR (AUTHOR_ID, AUTHOR_NAME) VALUES (?,?);", in_db)

#Book
cur.execute(""" 
    CREATE TABLE BOOK
        (BOOK_ID INTEGER PRIMARY KEY,
        BOOK_NAME TEXT) """)

with open('BOOK.csv','r') as lines:
    line = csv.DictReader(lines)
    in_db = [(i['BOOK_ID'], i['BOOK_NAME']) for i in line]

cur.executemany("INSERT INTO BOOK (BOOK_ID, BOOK_NAME) VALUES (?,?);", in_db)
				
#Library
cur.execute(""" 
    CREATE TABLE LIBRARY
        (ID INTEGER PRIMARY KEY,
        AUTHOR_ID INTEGER,
        BOOK_ID INTEGER) """)

with open('LIBRARY.csv','r') as lines:
    line = csv.DictReader(lines)
    in_db = [(i['ID'], i['AUTHOR_ID'], i['BOOK_ID']) for i in line]

cur.executemany("INSERT INTO LIBRARY (ID, AUTHOR_ID, BOOK_ID) VALUES (?,?,?);", in_db)

source.commit()

#Close the connection
source.close()