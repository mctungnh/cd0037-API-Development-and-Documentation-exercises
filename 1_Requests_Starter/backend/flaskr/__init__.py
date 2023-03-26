import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book, db

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

    @app.route('/')
    def home():
        return "hello"

    @app.route('/books')
    def get_books():
        booksPerPage = 8
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * booksPerPage
        end = start + booksPerPage
        
        books = Book.query.order_by(Book.id).all()
        formatted_books = [book.format() for book in books]
        return jsonify({
            "books": formatted_books,
            "success": True,
            "total_books": len(books),
        })

    @app.route("/books/<int:id>", methods=["GET", "PATCH"])
    def update_rating(id):
        book = Book.query.filter(Book.id == id).one_or_none()
        if book is None:
            abort(400)

        if request.method == "GET":
            return jsonify({"success": True, "book": book.format()})
        else:
            failed = False
            rating = request.args.get("rating", 0, type=int)
            try :
                book.rating = rating
                book.update()
            except:
                db.session.rollback()
                failed = True
            finally:
                db.session.close()

            if failed:
                abort(503)

            return jsonify(
                {
                    "success": True,
                    # "book": book.format()
                }
            )
        

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()
        if book is None:
            abort(400)
        
        try:
            book.delete()
        except:
            return(503)
        finally:
            db.session.close()
            
        books = Book.query.order_by(Book.id).all()
        formatted_books = [book.format() for book in books]
        
        return jsonify({
            "success": True,
            "deleted": book_id,
            "books": formatted_books,
            "total_books": len(formatted_books)
        })
        
    
    @app.route("/books", methods=["POST"])
    def create_book():
        book = Book(
            title=request.args.get("title", "untitled", type=str),
            author=request.args.get("author", "untitled", type=str),
            rating=request.args.get("rating", 0, type=int),
        )
        try:
            book.insert()
        except:
            return(503)
        finally:
            db.session.close()
            
        books = Book.query.order_by(Book.id).all()
        formatted_books = [book.format() for book in books]
        
        return jsonify({
            "success": True,
            # "created": book.id,
            "books": formatted_books,
            "total_books": len(formatted_books)
        })

    return app
