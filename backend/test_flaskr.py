import os
import unittest
import json
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
        self.database_path = f"postgresql://{'postgres'}:{'sirnusi'}@{'localhost:5432'}/{self.database_name}"


        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Highest goalscorer in Champions League?',
            'answer': 'Ronaldo',
            'category': '6',
            'difficulty': 5
        }
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
    
    
    # def test_to_get_all_categories(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['category'])

    # def test_404_for_getting_wrong_categories(self):
    #     res = self.client().get('/categories/999')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    
    # def test_to_get_paginated_questions(self):
    #     res = self.client().get('/questions')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
        
    # def test_404_to_get_beyond_page(self):
    #     res = self.client().get('/questions?page=1000')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    
    # def test_to_delete_specific_question(self):
    #     res = self.client().delete('/questions/3')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
    
    def test_404_for_making_wrong_delete(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    # def test_for_creating_a_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    
    # def test_405_for_creating_plant_not_allowed(self):
    #     res = self.client().post('/questions/45', json=self.new_question)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")

    
    # def test_for_searching_questions(self):
    #     new_search = {'searchTerm': 'autobiography'}
    #     res = self.client().post('/questions', json=new_search)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    
    # def test_404_for_searching_wrong_question(self):
    #     new_search = {'searchTerm': 'lq'}
    #     res = self.client().post('/questions', json=new_search)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_for_questions_based_on_category(self):
    #     res = self.client().get('categories/1/questions')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['current_category'])
    
    # def test_404_for_getting_questions_not_in_a_category(self):
    #     res = self.client().get('categories/10000/questions')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

   
      
    # def test_to_play_for_quiz_(self):
    #     json_play_quizz = {
    #         'previous_questions' : [],
    #         'quiz_category' : {
    #             'type' : 'Sport',
    #             'id' : '6'
    #             }
    #     } 
    #     res = self.client().post('/quizzes', json = json_play_quizz)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    # def test_400_get_quiz(self):
    #     res = self.client().post('/quizzes',
    #                              json={
    #                                  'previous_questions': []
    #                              })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'bad request')

   
   
   # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()