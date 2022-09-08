import os
import unittest
import json, requests
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("uncle-sam", "1234", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question= {"question": "Who is the first black president in USA ?", "answer": "Barack Obama", "difficulty": 1, "category":4}

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_get_categories(self):
    #     """Given a web user, when he hits /categories with a get request, then the response should have a status code of 200"""
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['categories']))

    # def test_get_paginated_questions(self):
    #     """Given a web user when he hits /questions with a get request, then the response should have a status code of 200"""
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(len(data['categories']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['current_category'])

    # def test_get_questions_in_specific_category(self):
    #     """Given a web user when he hits categories/category_id/questions with a valid category id and a get request, then the response should have a status code of 200"""
    #     res = self.client().get('/categories/5/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertEqual(data['total_questions'], 2)
    #     self.assertEqual(data['current_category'], 5)    
    
    # def test_post_question(self):
    #     """Given a web user, when he hits /questions with a post request, then the response should have a status code of 200"""
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(len(data['categories']))

    # def test_search_question(self):
    #     """Given a web user, when he hits /questions with search term and a post request, then the response should have a status code of 200"""
    #     res = self.client().post('/questions', json={"searchTerm":"boxer"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertEqual(data['total_questions'], 1)
    #     self.assertEqual(data['current_category'], 4)

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 2).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 2)
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(question, None)
        
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={"quiz_category" : {"id":5},"previous_questions":[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()