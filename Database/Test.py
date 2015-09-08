#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# A library that provides accessing the database
import sqlite3

source = sqlite3.connect('sourse.db')
cur = source.cursor()

l = []
#Check the import
for row in source.execute('''SELECT A.AUTHOR_NAME,
                                    B.BOOK_NAME
                             FROM AUTHOR A,
                                  BOOK B,
                                  LIBRARY L
                             WHERE L.BOOK_ID = B.BOOK_ID
                             AND L.AUTHOR_ID = A.AUTHOR_ID'''):
    l.append(row)
print(l, end='\n')
#Close the connection
source.close()

