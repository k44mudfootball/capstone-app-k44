# capstone-app-k44

## Casting Agency App

For the FSND capstone project, I decided to go with the default Casting Agency specification. This app allows company executives to manage Actors and Movies with Role Based Access Control (RBAC) 

### Accessing the App
The code is saved on Github, which is automatically deployed to Render.  There is no front end associated with this project - backend only.  See API Documentation section to access hosted app.

### Local run instructions
If you need to run locally, create a virtual environment with python 3.7 and pip install the dependencies in requirements.txt.  Run the run_db_clear.sh script which drops any existing DB, creates a new one, sets the environment variables in 'setup.sh' and starts the app.

### Running a test
If you need to run a test locally, create a virtual environment with python 3.7 and pip install the dependencies in requirements.txt. Run the run_test.sh script which drops any existing DB, creates a new one, sets the environment variables in 'test_setup.sh' and starts the test.

### Files included
#### Backend
1. `app.py` - Defines the API behavior
2. `models.py` - Initiates and defines the db table used
3. `auth\auth.py` - Handles authentication of REST requests with JWT tokens
4. `auth\__init__.py` - Required file to run
5. `requirements.txt` - Defines the python dependencies for 

#### Local Run support files
1. `db_data.sh` - Runs the 'db_data.sql' to populate the database
2. `db_data.sql` - INSERT statements to seed the database
3. `setup.sh` - sets environment variables.
4. `run_db_clear.sh` - Clears existing DB, ru

#### Test Files
1. `test.py` - Contains the unit tests
2. `run_test.sh` - Script to run the test.  
3. `test_setup.sh` - Sets the environment variables needed for test, including JWTs for the 3 roles

#### Authentication Files
1. `JWTs.txt` - Includes valid JWTs for each of the 3 roles to use when accessing the app via CURL commands.
2. `auth_config.sh` - When run, sets the following as environment variables: AUTH0_DOMAIN, CLIENT_ID, and JWT_SIGNING_SECRET.


# API Documentation
The URL of the hosted app is https://render-deployment-example-mtst.onrender.com/

## Authentication
Authentication for the app is 3rd party managed by Auth0. Because there is no frontend to the app, access is through Machine-to-Machine REST requests. The app uses RBAC with three separate roles defined: Executive Director, Casting Director, Casting Assistant.  Just prior to submital of the project, a JWT was generated for a user that has each of these roles, which has been put in `JWTs.txt`. In the endpoints below, replace {token} with one of these tokens. Note that the JWT tokens are valid for only 24 hours for new ones will need to be generated if a re-submittal is needed.

## Endpoints

### GET /actors
- General: Returns the list of actors
- `curl https://render-deployment-example-mtst.onrender.com/actors -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Will Smith",
      "gender": "Male",
      "age": 45,
    },
    {
      "id": 2,
      "name": "Bill Murray",
      "gender": "Male",
      "age": 67,
    },
    {
      "id": 3,
      "name": "Jennifer Laurence",
      "gender": "Female",
      "age": 35,
    },
    {
      "id": 4,
      "name": "Meryl Streep",
      "gender": "Female",
      "age": 80,
    },
  ],

}

```

### DELETE /actors/{int:actor_id}
- General:
    - Deletes the actor if the given id exists. Returns the id of the deleted actor and success value. 
- `curl -X DELETE https://render-deployment-example-mtst.onrender.com/actors -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
"success": true,
"deleted": 4,
}
```

### POST /actors
- General:
    - Creates a new question with provided question, answer, category, and difficulty. Returns the new question id, success value, question, answer, category, and difficulty. 
- `curl https://render-deployment-example-mtst.onrender.com/actors -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{"name": "Mike Wallen","gender": "Male","age": 23}' -H "Authorization: Bearer {token}"`
```
{
    "age": 23,
    "created": 5,
    "gender": "Male",
    "name": "Mike Wallen",
    "success": true
}

```

### PATCH /actors/{int:patch_id}
- General:
    - Creates a new question with provided question, answer, category, and difficulty. Returns the new question id, success value, question, answer, category, and difficulty. 
- `curl https://render-deployment-example-mtst.onrender.com/actors -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"name": "Mike Wallen","gender": "Male","age": 23}' -H "Authorization: Bearer {token}"`
```
{
    "age": 23,
    "created": 5,
    "gender": "Male",
    "name": "Mike Wallen",
    "success": true
}

```

### GET /categories/<int:category_id>/questions
- General:
    - Returns a list of questions, current category, success value, and number of questions that belong to a single category.
- `curl http://127.0.0.1:5000/categories/3/questions`

```
{
  "currentCategory": "Geography",
  "questions": [
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
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "I am he",
      "category": 3,
      "difficulty": 2,
      "id": 33,
      "question": "who am i?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```
### POST /quizzes
- General:
    - When provided a quiz category and a list of previous questions, returns a randomized question from that set.
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2,4,3], "quiz_category": {"id":2}}'`

```
{
  "question": {
    "answer": "Escher",
    "category": 2,
    "difficulty": 1,
    "id": 16,
    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  },
  "success": true
}
```

## Error Handling
Errors are returned as JSON objects in the following example:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five different types of errors during failures:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 
- 500: Internal server error

