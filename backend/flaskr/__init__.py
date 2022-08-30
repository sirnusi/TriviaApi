import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    books = [book.format() for book in selection]
    
    current_books = books[start:end]

    return current_books
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    # returning a list of categories.
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        
        # checking for empty categories to give a 404 error.
        if len(categories) == 0:
            abort(404)
            
        return jsonify({
            "success": True,
            "category": {category.id: category.type for category in categories}
        })
    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    # to get a list of the questions from the database 
    @app.route('/questions')
    def get_questions():
        question = Question.query.all()
        paginate_question = paginate_books(request, question)
        
        # checking if there is no question to give the 404 error
        if len(paginate_question) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "questions": paginate_question,
            "total_questions": len(question)
        })
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    # to delete a specific ID in the database.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_a_specific_question(question_id):
        try:
            #getting the questions by ID and then deleting with the delete()
            question = Question.query.get_or_404(question_id)
            question.delete()
            
            return jsonify({
                "success": True,
                "deleted": question.id
            })
            
        except:
            abort(404)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # creating a new question.
    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()
        
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        
        
        try:
            #binding the value gotten from the form to the Question model.
            question = Question(question=new_question, 
                                answer=new_answer, 
                                category=new_category,
                                difficulty=new_difficulty)
                
            question.insert()
            
            return jsonify({
                "success": True,
                "created": question.id,
                
            })
        except:
            abort(400)
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    # searching the database for questions
    @app.route('/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if search_term:
            # searching by the form 'searchTerm' and checking it 
            # for case sensitivity with the ilike()
            results_for_search = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                
            if not results_for_search:
                abort (404)    
                    
            paginate_question = paginate_books(request, results_for_search)
            return jsonify({
                'success': True,
                'questions': paginate_question,
                'total_questions': len(results_for_search)
            })             
             
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    # getting questions based on a particular category.
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        
        # filtering it by the category field in the Question model to 
        # the category_id(Category model)
        questions = Question.query.filter_by(category=str(category_id)).all()    
        
        if not questions:
            abort (404)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })
        
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    # trying to play quiz for a particular category.
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            data = request.get_json()
            quiz_category = data.get('quiz_category', None)
            category_id = quiz_category["id"]
            previous_questions = data.get('previous_questions', None)

            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()

            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()

            if questions:
                question = random.choice(questions)
            else:
                question = None

            formatted_question = question.format()

            return jsonify({
                'success': True,
                'question': formatted_question
            })

        except BaseException:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app

