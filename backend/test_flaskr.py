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
    def test_get_categories(self):
        """Given a web user, when he hits /categories with a get request, then the response should have a status code of 200"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        """Given a web user when he hits /questions with a get request, then the response should have a status code of 200"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_404_requesting_invalid_page(self):
        """Given a web user, when he hits  : /questions?page=invalid_number_of_page with get request, then the response should have a status code of 404
        and the response body should contain the expected payload"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")

    def test_get_questions_in_specific_category(self):
        """Given a web user when he hits categories/category_id/questions with a valid category id and a get request, then the response should have a status code of 200"""
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], 5)  

    def test_404_get_questions_in_invalid_category(self):
        """Given a web user when he hits categories/category_id/questions with a invalid category id and a get request, then the response should have a status code of 200"""
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")    
    
    def test_post_question(self):
        """Given a web user, when he hits /questions with a post request, then the response should have a status code of 200"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_405_posting_questions_not_allowed(self):
        "Given a web user, when he hits bad url with post request, and provides a json question information, then the response should have a status code : 405"
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")

    def test_search_question(self):
        """Given a web user, when he hits /questions with search term and a post request, then the response should have a status code of 200"""
        res = self.client().post('/questions', json={"searchTerm":"boxer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 1)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "bobiliapplejacks"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(question, None)
    
    def test_delete_unexisting_question(self):
        "Given a web user, when he hits /questions/question_id with delete request, if the question_id doesn't exist in then db, then the response should have a status code : 422"
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
        
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={"quiz_category" : {"id":5},"previous_questions":[]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()