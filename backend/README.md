## Introduction

### Getting started
- Base URL: This app runs locally on the port 5000 `http://127.0.0.1:500`.
- Authentication: There is currrently no authentication in my project.

### Error Handling 
Errors return JSON objects in the following format:
``` {
  "success": False,
  "error": 404,
  "message": "resource not found"
}
```

In this Trivia API Project it will return four(4) types of error when the request fails:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable entity

### Endpoints
#### GET /categories
- General
  - Returns a list of categories and a success message
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    "category": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

```

#### GET /questions
- General:
  -  Returns a list of questions 10 per page, success value, and total number of questions
  - Results are paginated in 2s. Include a request argument to choose page number, starting from 1.
- Sample `curl http://127.0.0.1:5000/questions`
```
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
}

```


#### DELETE /plants/{question_id}
- General:
    - Deletes question if it exists in the database. Returns id of the deleted plant.
- `curl -X DELETE http://127.0.0.1:5000/questions/14`

```
{
    "deleted": 14,
    "success": true
}

```


#### POST /questions
- General:
    - Creates a question given the objects of the database which are question, answer, category, difficulty.
- ` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{"question":"Best Player", "answer":"Ronaldo", "category":"6", "difficulty":"5"}"`

```
{
    "created": 24,
    "success": true
}

```


#### POST /search
- General:
    - searches for questions in the database. Returns a list of the searched object, total number of questions with a success message.
- ` curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"best player"}'`

```
{
    "questions": [
        {
            "answer": "Ronaldo",
            "category": 6,
            "difficulty": 5,
            "id": 24,
            "question": "Best Player"
        },
        {
            "answer": "Ronaldo",
            "category": 6,
            "difficulty": 5,
            "id": 25,
            "question": "Best Player"
        }
    ],
    "success": true,
    "total_questions": 2
}

```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions for a particular category, the current category and a total number of questions in that category
    - Results are paginated in 2s. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/6/questions`

```
{
    "current_category": 6,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Ronaldo",
            "category": 6,
            "difficulty": 5,
            "id": 24,
            "question": "Best Player"
        },
        {
            "answer": "Ronaldo",
            "category": 6,
            "difficulty": 5,
            "id": 25,
            "question": "Best Player"
        }
    ],
    "success": true,
    "total_questions": 4
}

```

### GET /quizzes

- Getting a random question within a chosen category
- URI: `curl http://127.0.0.1:5000/quizzes`