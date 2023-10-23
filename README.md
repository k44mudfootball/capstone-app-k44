# capstone-app-k44

## Casting Agency App

For the FSND capstone project, I decided to go with the default Casting Agency specification. This app allows company executives to manage Actors and Movies with Role Based Access Control (RBAC) 

### Accessing the App
The app is hosted and automatically deployed by Render (render.com) upon code changes in the Github repository.  There is no front end associated with this project - backend only.  See API Documentation section to access the hosted version of the app.

### Local run instructions
If you need to run locally, create a virtual environment with python 3.7 and pip install the dependencies in requirements.txt.  Run the run_db_clear.sh script which drops any existing DB, creates a new one, sets the environment variables in 'setup.sh' and starts the app.

### Running a test
If you need to run a test locally, create a virtual environment with python 3.7 and pip install the dependencies in requirements.txt. Run the run_test.sh script which drops any existing DB, creates a new one, sets the environment variables in 'test_setup.sh' and starts the test.

### Files included
The code is stored on Github in the https://github.com/k44mudfootball/capstone-app-k44 public repository

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
2. `auth_config.sh` - When run, exports the following as environment variables: AUTH0_DOMAIN, CLIENT_ID, and JWT_SIGNING_SECRET.

# API Documentation
The URL of the hosted app is https://render-deployment-example-mtst.onrender.com/

## Authentication
Authentication for the app is 3rd party managed by Auth0. Because there is no frontend to the app, access is through Machine-to-Machine REST requests. The app uses RBAC with three separate roles defined: Executive Producer, Casting Director, Casting Assistant.  Just prior to submital of the project, a JWT was generated for a user that has each of these roles, which has been put in `JWTs.txt`. In the endpoints below, replace {token} with one of these tokens. Note that the JWT tokens are valid for only 24 hours for new ones will need to be generated if a re-submittal is needed.

## Endpoints

### GET /actors
- General: Returns the list of actors
- Permitted roles: Executive Producer, Casting Director, Casting Assistant

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
  ]

}

```

### DELETE /actors/{int:actor_id}
- General:
    - Deletes the actor if the given id exists. Returns the id of the deleted actor and success value. 
- Permitted roles: Executive Producer, Casting Director

- `curl -X DELETE https://render-deployment-example-mtst.onrender.com/actors/4 -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
"success": true,
"deleted": 4,
}
```

### POST /actors
- General:
    - Creates a new actor with provided name, gender, and age. Returns the new actor id, success value, name, gender, and age.
- Permitted roles: Executive Producer, Casting Director

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

### PATCH /actors/{int:actor_id}
- General:
    - Updates an existing actor's details including name, gender, or age.  Any combination of fields can be passed.  Success is returned.
- Permitted roles: Executive Producer, Casting Director

- `curl https://render-deployment-example-mtst.onrender.com/actors/2 -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"name": "Ted Wallen"}' -H "Authorization: Bearer {token}"`

- `curl https://render-deployment-example-mtst.onrender.com/actors/2 -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"gender": "Female"}' -H "Authorization: Bearer {token}"`

- `curl https://render-deployment-example-mtst.onrender.com/actors/2 -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"age": 34}' -H "Authorization: Bearer {token}"`
```
{
    "success": true
}

```
### GET /movies
- General: Returns the list of movies
- Permitted roles: Executive Producer, Casting Director, Casting Assistant

- `curl https://render-deployment-example-mtst.onrender.com/movies -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "The Big Lebowski",
      "release_date": "Sun, 25 Mar 2012 00:00:00 GMT"
    },
    {
      "id": 2,
      "title": "Star Wars",
      "release_date": "Sun, 25 Mar 1977 00:00:00 GMT"
    },
    {
      "id": 3,
      "title": "Return of the Jedi",
      "release_date": "Sun, 25 Mar 1980 00:00:00 GMT"
    },
    {
      "id": 4,
      "title": "The Empire Strikes Back",
      "release_date": "Sun, 25 Mar 1983 00:00:00 GMT"
    }
  ]

}

```

### DELETE /movies/{int:movie_id}
- General:
    - Deletes the movie if the given id exists. Returns the id of the deleted movie and success value. 
- Permitted roles: Executive Producer

- `curl -X DELETE https://render-deployment-example-mtst.onrender.com/movies/4 -H "Accept: application/json" -H "Authorization: Bearer {token}"`

``` {
"success": true,
"deleted": 4,
}
```

### POST /movies
- General:
    - Creates a new movie with provided title and release date. Returns the new movie id, success value, title, and release date.
- Permitted roles: Executive Producer

- `curl https://render-deployment-example-mtst.onrender.com/movies -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{"title": "Akira","release_date": "1990-03-25"}' -H "Authorization: Bearer {token}"`
```
{
    "id": 5,
    "title": "Akira",
    "release_date": "Sun, 25 Mar 1990 00:00:00 GMT"
    "success": true,
}

```

### PATCH /movies/{int:movie_id}
- General:
    - Updates an existing movie's details including title and release date.  Any combination of fields can be passed.  Success is returned.
- Permitted roles: Executive Producer, Casting Director

- `curl https://render-deployment-example-mtst.onrender.com/movies/2 -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"title": "Rogue One"}' -H "Authorization: Bearer {token}"`

- `curl https://render-deployment-example-mtst.onrender.com/movies/2 -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -d '{"release_date": "1992-03-25"}' -H "Authorization: Bearer {token}"`

```
{
    "success": true
}

```

## Error Handling
Errors are returned as JSON objects in the following example:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return seven different types of errors during failures:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 
- 500: Internal server error

