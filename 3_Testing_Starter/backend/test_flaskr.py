import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            "postgres", "localhost:5432", self.database_name
        )
        # setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!
    def test_retrive_books(self):
        """Test retive books"""
        res = self.client().get('/books')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["total_books"], (len(Book.query.all())))
        
        res = self.client().get('/books?page=1000')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json["success"], False)
        self.assertEqual(res.json["error"], 404)
        self.assertEqual(res.json["message"], "resource not found")
    
    def test_update_book(self):
        """Test update book"""
        res = self.client().patch("/books/1", json={"rating": 1})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(book.format()["rating"], 1)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
