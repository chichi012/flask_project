from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer)

    # def database_books(self):
    #     ls_of_books = ['In Search of Lost Time by Marcel Proust', 'Ulysses by James Joyce','Don Quixote by Miguel de Cervantes','One Hundred Years of Solitude by Gabriel Garcia Marquez', 'The Great Gatsby by F.','Moby Dick by Herman Melville',' War and Peace by Leo Tolstoy','Hamlet by William Shakespeare']
    #     prices_list = [23.77, 12.99, 25.12, 67.00, 10.99, 9.99, 3.99, 4.66]
    #     isbn_list = [1234, 5678, 910012, 1234567, 192021222, 233456767, 567789674,59675467332]
    # element = [[x, y, z] for x, y, z in zip(ls_of_books, prices_list, isbn_list)]
    # for i in range(len(element)):
        # Book.add_book(element[i][0], element[i][1], element[i][2])

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

    def add_book(_name, _price, _isbn):
        # the underscores '_' before the '_name' means what was passed into the function
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]
        # Book() class has the db.Model properties (eg query) and this function can inherit that

    def get_book(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    def delete_book(_isbn):
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        # after delete we need to save
        db.session.commit()
        return bool(is_successful)

    def update_book_price(_isbn, _price):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        db.session.commit()

    def update_book_name(_isbn, _name):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        db.session.commit()

    def replace_book(_isbn, _name, _price):
        book_to_replace = Book.query.filter_by(isbn=_isbn).first()
        book_to_replace.name = _name
        book_to_replace.price = _price
        db.session.commit()

    def __repr__(self):
        # representation method of how it looks in the terminal
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)

    #  from book_model import *
    # Book.get_all_books()
