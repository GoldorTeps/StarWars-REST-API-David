"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Starships, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///example.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

with app.app_context():
    db.create_all()


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    try:
        return render_template("index.html")
    except:
        return generate_sitemap(app)


# GET Methods
@app.route("/users", methods=["GET"])
def users_get():
    user_list = User.query.all()
    return jsonify([user.serialize() for user in user_list]), 200


@app.route("/users", methods=["POST"])
def user_post():
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'email' not in body:
        raise APIException("You need to specify the email", status_code=400)
    if 'password' not in body:
        raise APIException("You need to specify the password", status_code=400)

    user = User(email=body['email'], password=body['password'], is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200


@app.route("/users/favorites", methods=["GET"])
def favorites_get():
    # In a real app we would get the user from the session/token
    # For this exercise, we'll use the first user in the DB
    user = User.query.first()
    if user is None:
        return jsonify({"msg": "No users found"}), 404
    
    favorites = Favorites.query.filter_by(user_id=user.id).first()
    if favorites is None:
        return jsonify([]), 200
        
    return jsonify(favorites.serialize()), 200


@app.route("/people", methods=["GET"])
def people_get():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route("/people/<int:person_id>", methods=["GET"])
def person_get(person_id):
    person = People.query.get(person_id)
    if person is None:
        raise APIException("Person not found", status_code=404)
    return jsonify(person.serialize()), 200


@app.route("/planets", methods=["GET"])
def planets_get():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def planet_get(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200


@app.route("/starships", methods=["GET"])
def starships_get():
    starships = Starships.query.all()
    return jsonify([ship.serialize() for ship in starships]), 200


@app.route("/starships/<int:starship_id>", methods=["GET"])
def starship_get(starship_id):
    starship = Starships.query.get(starship_id)
    if starship is None:
        raise APIException("Starship not found", status_code=404)
    return jsonify(starship.serialize()), 200


# POST Methods for Favorites
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user = User.query.first()
    if user is None: return jsonify({"msg": "User not found"}), 404
    
    planet = Planets.query.get(planet_id)
    if planet is None: return jsonify({"msg": "Planet not found"}), 404

    favs = Favorites.query.filter_by(user_id=user.id).first()
    if favs is None:
        favs = Favorites(user_id=user.id)
        db.session.add(favs)
    
    if planet not in favs.planets:
        favs.planets.append(planet)
        db.session.commit()
    
    return jsonify(favs.serialize()), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user = User.query.first()
    if user is None: return jsonify({"msg": "User not found"}), 404
    
    person = People.query.get(people_id)
    if person is None: return jsonify({"msg": "Person not found"}), 404

    favs = Favorites.query.filter_by(user_id=user.id).first()
    if favs is None:
        favs = Favorites(user_id=user.id)
        db.session.add(favs)
    
    if person not in favs.people:
        favs.people.append(person)
        db.session.commit()
    
    return jsonify(favs.serialize()), 200


# DELETE Methods for Favorites
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user = User.query.first()
    favs = Favorites.query.filter_by(user_id=user.id).first()
    if favs is None: return jsonify({"msg": "Favorites not found"}), 404
    
    planet = Planets.query.get(planet_id)
    if planet in favs.planets:
        favs.planets.remove(planet)
        db.session.commit()
    
    return jsonify(favs.serialize()), 200


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    user = User.query.first()
    favs = Favorites.query.filter_by(user_id=user.id).first()
    if favs is None: return jsonify({"msg": "Favorites not found"}), 404
    
    person = People.query.get(people_id)
    if person in favs.people:
        favs.people.remove(person)
        db.session.commit()
    
    return jsonify(favs.serialize()), 200


# DELETE Methods
@app.route("/planet/<int:position>", methods=["DELETE"])
def delete_planet(position):
    print(f"delete planets in position {position}")
    return jsonify(position)


@app.route("/people/<int:position>", methods=["DELETE"])
def delete_person(position):
    print(f"delete people in position {position}")
    return jsonify(position)


@app.route("/starships/<int:position>", methods=["DELETE"])
def delete_startship(position):
    print(f"delete starships in position {position}")
    return jsonify(position)