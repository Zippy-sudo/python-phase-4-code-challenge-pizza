#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):

    def get(self):
        restaurants_dict = [restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in Restaurant.query.all()]
        response = make_response(restaurants_dict, 200)
        return response
    
api.add_resource(Restaurants, '/restaurants')

class RestaurantsByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id = id).first()
        if restaurant:
            response = make_response(restaurant.to_dict(), 200)
            return response
        else:
            return make_response({"error": "Restaurant not found"}, 404)
    
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id = id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({},204)
        else:
            return make_response({"error": "Restaurant not found"}, 404)
    
api.add_resource(RestaurantsByID, '/restaurants/<int:id>')

class Pizzas(Resource):

    def get(self):
        pizzas_list = [pizza.to_dict() for pizza in Pizza.query.all()]
        response = make_response(pizzas_list, 200)
        return response
    
api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):

    def post(self):
                if 1 <= int(request.get_json().get('price')) <= 30 and int(request.get_json().get('restaurant_id')) and int(request.get_json().get('pizza_id')):
                    to_post = RestaurantPizza(
                        price=request.get_json().get('price'),
                        restaurant_id = request.get_json().get('restaurant_id'),
                        pizza_id = request.get_json().get('pizza_id')
                        )
                    db.session.add(to_post)
                    db.session.commit()
                    response_dict = to_post.to_dict()
                    response = make_response(response_dict, 201)
                else:
                    response = make_response({"errors": ["validation errors"]},400)
                return response

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
