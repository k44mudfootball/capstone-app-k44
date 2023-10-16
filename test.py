import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
#from dotenv import load_dotenv

class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        #Load the DB secret info
        database_url = os.environ['DATABASE_URL']
        """
        load_dotenv(override=True)
        db_username=os.getenv("DB_USERNAME")
        db_password=os.getenv("DB_PASSWORD")
        db_host=os.getenv("DB_HOST")
        """

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres_test"
        #self.database_path = 'postgresql://{}:{}@{}/{}'.format(db_username, db_password, db_host, self.database_name)
        self.database_path = database_url
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Who is the best tester?", "answer": "She is the best test", "category": 4, "difficulty": 1}
        self.bad_new_question = {"question":1, "answer": None, "category": "i am a string", "difficulty": [2,3,4]}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """

    #---------------------
    #/categories Endpoint
    #---------------------
    #Success
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    #Error - 404 resource not found
        res = self.client().get("/categories/10")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    #Error - 405 method not allowed
    def test_405_error_categories(self):
        res = self.client().delete('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    #---------------------
    #/questions Endpoint
    #---------------------
    # Success - Get
    def test_get_questions(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["currentCategory"], None)

    #400 bad request get
    def test_400_error_get_questions(self):
        res = self.client().get("/questions?page=100000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # Success - Post
    def test_add_question(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)
        
        #This adds a new entry to the trivia_test database which
        #will be used by the successful delete case
        global added_book_id
        added_book_id = data["created"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["question"]))
        self.assertTrue(data["answer"])
        self.assertTrue(data["category"])
        self.assertTrue(data["difficulty"])

    #422 Post
    def test_422_error_post_question(self):
        res = self.client().post('/questions',json=self.bad_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #---------------------
    #'/questions/<int:question_id>' endpoint
    #--------------------
    # Success - Delete
    def test_delete_question(self):
        test_question=Question.query.get(added_book_id)
        #print("test_question = {}".format(test_question.id))

        res = self.client().delete("/questions/{}".format(added_book_id))
        data = json.loads(res.data)

        question=Question.query.get(added_book_id)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], added_book_id)
        self.assertEqual(question, None)

    #422 Delete
    def test_422_error_delete_question(self):
        res = self.client().delete("/questions/1000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    #405 Delete
    def test_405_error_delete_question(self):
        res = self.client().post('/questions/1')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    #---------------------
    #'/questions/search' endpoint
    #--------------------
    # Success - Post Search with results
    def test_search_question_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "Penicillin"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(len(["total_questions"]),1)
        self.assertEqual(data["currentCategory"], None)

    # Success - Post Search no results
    def test_search_question_no_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "This will yield nothing"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertFalse(data["questions"])
        self.assertEqual(data["total_questions"],0)
        self.assertEqual(data["currentCategory"], None)

    #Error - 405 method not allowed
    def test_405_error_search(self):
        res = self.client().delete('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    #---------------------
    #'/categories/<int:category_d>/questions' endpoint
    #--------------------

    # Success
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["currentCategory"])

    #Error - 400 bad request
    def test_404_questions_by_category(self):
        res = self.client().get("/categories/10/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
    
    #Error - 405 method not allowed
    def test_405_error_questions_by_category(self):
        res = self.client().delete('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    #---------------------
    #'/quizzes' endpoint
    #--------------------

    # Success
    def test_quizzes(self):
        res = self.client().post("/quizzes", json={"previous_questions": [2,4,3], "quiz_category": {"id":2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    #422 error
    def test_422_error_quizzes(self):
        res = self.client().post("/quizzes", json={"previous_questions": [2,4,3], "quiz_category": {}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #Error - 405 method not allowed
    def test_405_error_quizze(self):
        res = self.client().delete('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    """
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()