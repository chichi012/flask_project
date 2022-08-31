import json
from flask import Flask, jsonify, request, Response
from settings import *
'''
1. Build first flask application API 
2. First end-point '/books'
3. Second end-point '/books/<ISBN>
'''
#
# app = Flask(__name__)
books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {'name': 'The Cat In the Hat',
     'price': 6.99,
     'isbn': 9782371000193}

]


# GET /books is default. To over-write this, eg
# @app.route('/books', method = ['POST'])
@app.route('/books')
def get_books():
    # return a json instead of a list
    return jsonify({'books': books})


# GET /books/9782371000193
@app.route('/books/<int:isbn>')
def get_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }

    return jsonify(return_value)


'''
1. Allow users to add books to store
2. Defined URI , how to pass in parameters
3. Handle different HTTP verbs (GET and POST)
4. Send back correct response code, content type, headers
2. But ensure the books data being added by clients is valid
'''


def valid_book_object(book_object):
    if "name" in book_object and "price" in book_object and "isbn" in book_object:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
def add_books():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        # a Location header points to where the client can go and receivee the new resource that was created
        # expected link is /books/isbn_number
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response  # response status code 200
    else:
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "help_string": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 1234567890}"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response


'''
1. Allow clients to update books in our store using PUT route
PUT /books/978039400165
  {
            "name": "The Odessey",
            "price": 7.99
        }
a. no valid book object from client
--> not add the book to the store

b. valid book object has name and price field 
        
'''


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        "name": request_data['name'],
        "price": request_data['price'],
        "isbn": isbn
    }
    # create a loop to search for the book in books
    i = 0
    for book in books:
        current_isbn = book["isbn"]
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


'''
1. PATCH: allow clients to update a certain attribute eg to update only 'name' of book in store
eg from
  {
            "name": "The Odessey",
            "price": 7.99
            
    }
    
    to 
    
      {
            "name": "The Odessey Part 2",
            "price": 7.99
'''


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    # updated_book will serve as a placeholder for all different properties that need updating
    updated_book = {}
    if ("name" in request_data):
        updated_book["name"] = request_data["name"]
    if ("price" in request_data):
        updated_book["price"] = request_data["price"]
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


'''
1. DELETE HTTP method , allow clients to delete a book
- delete the isbn since its unique
-no need to send a body in postman
'''


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book['isbn'] == isbn:
            # return jsonify(book)
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalid_book_object_error_msg = {
        "error": "Book with the ISBN Number that was provided was not found, therefore unable to delete"}
    response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype="application/json")
    return response


''' 
STORING DATA IN A SQL DATABASE
settings.py file will store the configuration for the database
'''

app.run(port=5000)
