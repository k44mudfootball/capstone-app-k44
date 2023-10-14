import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Actor, Movie
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

#  Actor Endpoints
#  ----------------------------------------------------------------

#  Get all actors
    @app.route('/actors')
    def get_actors():
        actors=Actor.query.all()

        if len(actors) == 0:
            abort(404)

        formatted_actors = [actor.format() for actor in actors]
        
        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

#  Delete an actor
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor=Actor.query.get(actor_id)
            
        #Deletes the actor, aborts 404 if actor ID is not found
        if actor is None:
            abort(404)
        else:
            actor.delete()
        
        #Returns the json object
        return jsonify({
            "success": True,
            "deleted": actor_id,
        })
    
#  Create a new actor
    @app.route('/actors',methods=['POST'])
    def create_actor():
        #Gets the json body and attributes from the form
        body = request.get_json()
        new_name = body.get("name", None)
        new_gender = body.get("gender", None)
        new_age = body.get("age", None)

        try:
            #Creates a new entry in the DB
            actor = Actor(name=new_name, gender=new_gender, age=new_age)
            actor.insert()

            #Returns the json object
            return jsonify(
                {
                    "success": True,
                    "created": actor.id,
                    "name": actor.name,
                    "gender": actor.gender,
                    "age": actor.age,
                }
            )

        except:
            abort(422)

# Update actor details
    @app.route("/actors/<actor_id>", methods=["PATCH"])
    def update_actor(actor_id):
        #Get body from Json
        body = request.get_json()

        try:
            #Find the actor by actor id
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            #Update name if included
            if "name" in body:
                actor.name = body.get("name")
            
            #Update gender if included
            if "gender" in body:
                actor.gender = body.get("gender")

            #Update age if included
            if "age" in body:
                actor.age = int(body.get("age"))

            #Apply to the DB
            actor.update()

            return jsonify(
                {
                    "success": True,
                }
            )

        except:
            abort(400)

    #  Movie Endpoints
    #  ----------------------------------------------------------------

    @app.route('/movies')
    def get_movies():
        movies=Movie.query.all()

        if len(movies) == 0:
            abort(404)

        formatted_movies = [movie.format() for movie in movies]
        
        return jsonify({
            'success': True,
            'actors': formatted_movies
        })    
    
    @app.route('/movies/<movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie=Movie.query.get(movie_id)
            
        #Deletes the actor, aborts 404 if actor ID is not found
        if movie is None:
            abort(404)
        else:
            movie.delete()
        
        #Returns the json object
        return jsonify({
            "success": True,
            "deleted": movie_id,
        })
    
    @app.route('/movies',methods=['POST'])
    def create_movie():
        #Gets the json body and attributes from the form
        body = request.get_json()
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)

        try:
            #Creates a new entry in the DB
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            #Returns the json object
            return jsonify(
                {
                    "success": True,
                    "created": movie.id,
                    "title": movie.title,
                    "release_date": movie.release_date
                }
            )

        except:
            abort(422)

    # Update movie details
    @app.route("/movies/<movie_id>", methods=["PATCH"])
    def update_movie(movie_id):
        #Get body from Json
        body = request.get_json()

        try:
            #Find the actor by actor id
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            #Update title if included
            if "title" in body:
                movie.title = body.get("title")
            
            #Update release date if included
            if "release_date" in body:
                movie.release_date = body.get("release_date")

            #Apply to the DB
            movie.update()

            return jsonify(
                {
                    "success": True,
                }
            )

        except:
            abort(400)

    #-----------  ERROR HANDLERS  --------------
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}),404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": 405, "message": "method not allowed"}),405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
