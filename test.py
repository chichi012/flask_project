def valid_book_object(book_object):
    if "name" in book_object and "price" in book_object and "isbn" in book_object:
        return True
    else:
        return False


valid_object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 9780394001467
}

missing_name = {
    'price': 7.99,
    'isbn': 978039400196
}

missing_price = {
    'name': 'G',
    'isbn': 97803940016523
}

missing_isbn = {
    'name': 'G',
    'price': 7.99,
}

empty_dict = {}