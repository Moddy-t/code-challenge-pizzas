#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def get_restaurants():
    restaurants =[]
    for restaurant in Restaurant.query.all():
        restaurant_dict ={
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurants.append(restaurant_dict)
        response = make_response(jsonify(restaurants), 200) 

    return response

@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        response = make_response(jsonify({'message': 'restaurant not found'}), 404)
        return response

    restaurant_dict = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'restaurant_pizzas': restaurant.restaurant_pizzas
    }
    response = make_response(jsonify(restaurant_dict), 200)
    return response

@app.route('/pizza')
def get_pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizzas.append(pizza_dict)
        response = make_response(jsonify(pizzas), 200)

    return response


@app.route('/pizza/<int:id>')   
def get_pizza(id):
    pizza = Pizza.query.filter_by(id=id).first()
    if pizza is None:
        response = make_response(jsonify({'message': 'pizza not found'}), 404)
        return response
    pizza_dict = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }
    response = make_response(jsonify(pizza_dict), 200)
    return response

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']
    price = data['price']

    if price < 1 or price > 30:
        response = make_response(jsonify({'error': ['validartion errors']}), 400)
        return response

    new_restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id, restaurant_id=restaurant_id, price=price)
    db.session.add(new_restaurant_pizza)
    db.session.commit()
    return make_response(jsonify({'errors': ['validartion errors']}), 201)


@app.route('/restaurant/<int:id>', methods=['DELETE'])   
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        response = make_response(jsonify({'errors': '["restaurant not found"]'}), 404)
        return response
    db.session.delete(restaurant)
    db.session.commit()
    return make_response(jsonify({'message': 'restaurant pizza deleted'}), 200)

    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
