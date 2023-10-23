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
        #Load Env variables
        database_url = os.environ['DATABASE_URL']
        jwt_exec_prod = os.environ['JWT_EXEC_PROD']
        jwt_cast_dir = os.environ['JWT_CAST_DIR']
        jwt_cast_asst = os.environ['JWT_CAST_ASST']

        #Define the app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres_test"
        self.database_path = database_url

        #Set the headers jwt variables
        self.jwt_exec_prod = jwt_exec_prod
        self.jwt_cast_dir = jwt_cast_dir
        self.jwt_cast_asst = jwt_cast_asst
        
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        

        # Seed the database
        self.actor1 = Actor(name="Actor name 1", gender="Male", age=56)
        self.actor1.insert()

        self.actor2 = Actor(name="Actor name 2", gender="Feale", age=36)
        self.actor2.insert()

        self.movie1 = Movie(title="movie_title1", release_date="1980-01-15")
        self.movie1.insert()

        self.movie2 = Movie(title="movie_title2", release_date="1985-01-15")
        self.movie2.insert()

        # Input json for the post tests
        self.new_actor1 = {
            "name": "Liam Neeson",
            "gender": "Male", 
            "age": 42
            }
        self.new_actor2 = {
            "name": "Jennifer Lawrence", 
            "gender": "Female", 
            "age": 26
            }
        self.bad_actor = {
            "gender": "Female", 
            "age": "I should be an integer"
            }
        self.new_movie1 = {
            "title": "The Best Movie Ever", 
            "release_date": "1980-01-15"
            }
        self.new_movie2 = {
            "title": "The Best Movie Ever 2", 
            "release_date": "2000-01-15"
            }
        self.bad_movie = {
            "release_date": "2020-01-15", 
            "bogus_field": "Ooops I added an extra field" 
            }

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    

    #---------------------
    #/actors Endpoint
    #---------------------
    # ---- POST ------
    # Success (Role: Casting Director)
    def test_add_actor(self):
        res = self.client().post('/actors',json=self.new_actor1,headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)
        
        #This adds a new entry to the test database which
        #will be used by the successful delete case
        global added_new_actor
        added_new_actor = data["created"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["name"])
        self.assertTrue(data["gender"])
        self.assertTrue(data["age"])

    # Success (Role: Executive Producer)
    def test_add_actor2(self):
        res = self.client().post('/actors',json=self.new_actor2,headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)
        
        #This adds a new entry to the test database which
        #will be used by the successful delete case
        global added_new_actor2
        added_new_actor2 = data["created"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["name"])
        self.assertTrue(data["gender"])
        self.assertTrue(data["age"])
 
    # Error 422 unprocessable (Role: Casting Assistant)
    def test_422_error_post_actor(self):
        res = self.client().post('/actors',json=self.bad_actor,headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Error 403 unauthorized (Role: Casting Assistant)
    def test_auth_error_post_actor(self):
        res = self.client().post('/actors',json=self.new_actor2,headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)

    # ---- PATCH ------
    # Success (Role: Executive Producer)
    def test_update_actor(self):
        res = self.client().patch('/actors/2',json={"name":"my new name"},headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Error 403 unauthorized (Role: Casting Assistant)
    def test_auth_error_update_actor(self):
        res = self.client().patch('/actors/2',json={"name":"my new name"},headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)

    #Error - 405 method not allowed
    def test_405_error_get_actors(self):
        res = self.client().get("/actors/10",headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # ---- GET ------
    # Success (Role: Casting Assistant)
    def test_get_actors(self):
        res = self.client().get('/actors',headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    #Error - 405 method not allowed
    def test_405_error_delete_actors(self):
        res = self.client().delete('/actors',headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # ---- DELETE ------
    # Success (Role: Casting Director)
    def test_delete_actor(self):
        res = self.client().delete("/actors/1",headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)

        actor=Actor.query.get(1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], "1")
        self.assertEqual(actor, None)

    #Error - 404 resource not found
    def test_404_error_delete_actor(self):
        res = self.client().delete("/actors/15",headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    #---------------------
    #/movies Endpoint
    #---------------------
    
    # ---- POST ------
    # Success (Role: Executive Producer)
    def test_add_movie(self):
        res = self.client().post('/movies',json=self.new_movie1,headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)

        global added_new_movie1
        added_new_movie1 = data["created"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["title"])
        #self.assertTrue(data["release_date"])

    # Success (Role: Executive Producer)
    def test_add_movie2(self):
        res = self.client().post('/movies',json=self.new_movie2,headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)

        global added_new_movie2
        added_new_movie2 = data["created"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["title"])
        #self.assertTrue(data["release_date"])

    # Error 422 unprocessable (Role: Executive Producer)
    def test_422_error_post_movie(self):
        res = self.client().post('/movies',json={},headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Error 403 unauthorized (Role: Casting Director)
    def test_auth_error_post_movie(self):
        res = self.client().post('/movies',json=self.new_movie2,headers=dict(Authorization='bearer ' + self.jwt_cast_dir))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)

    # ---- PATCH ------
    # Success (Role: Casting Director)
    def test_update_movie(self):
        res = self.client().patch('/movies/3',json={"release_date": "2015-02-02"}, headers=dict(Authorization='bearer ' + self.jwt_cast_dir))

        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Error 403 unauthorized (Role: Casting Assistant)
    def test_auth_error_update_movie(self):
        res = self.client().patch('/movies/1',json={"title":"my new title"},headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)


    #Error - 405 method not allowed (Role: Casting Assistant)
    def test_405_error_get_movies(self):
        res = self.client().get("/movies/10",headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    # ---- GET ------
    # Success (Role: Casting Assistant)
    def test_get_movies(self):
        res = self.client().get('/movies',headers=dict(Authorization='bearer ' + self.jwt_cast_asst))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    #Error - 405 method not allowed (Role: Exec Producer)
    def test_405_error_delete_movies(self):
        res = self.client().delete('/movies',headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # ---- DELETE ------
    # Success (Role: Casting Director)
    def test_delete_movie(self):
        res = self.client().delete("/movies/2",headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)

        movie=Movie.query.get(2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], "2")
        self.assertEqual(movie, None)

    #Error - 404 resource not found
    def test_404_error_delete_movie(self):
        res = self.client().delete("/movies/15",headers=dict(Authorization='bearer ' + self.jwt_exec_prod))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()