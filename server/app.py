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
    restaurants = []
    # loop through all of the restaurants in the database
    restaurants =[]
    for restaurant in Restaurant.query.all():
        # create a dictionary to hold the information about the restaurant
        restaurant_dict ={
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        # add the dictionary to the list of restaurants
        restaurants.append(restaurant_dict)
    # create a response from the list of restaurants
    response = make_response(jsonify(restaurants), 200)
    return  response

@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    # search for a restaurant in the database by its id
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        # if a restaurant is not found, create an error message
        response = make_response(jsonify({'error': 'Restaurant not found'}), 404)
        return response
    # create a dictionary from the restaurant's information
    restaurant_dict = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'restaurant_pizzas': restaurant.restaurant_pizzas
    }
    # make a response from the dictionary
    response = make_response(jsonify(restaurant_dict), 200)
    return response

@app.route('/pizzas')
def get_pizzas():
    # create an empty list to hold a list of dictionaries representing pizzas
    pizzas = []
    # loop through all of the pizzas in the database
    for pizza in Pizza.query.all():
        # create a dictionary to hold the information about the pizza
        pizza_dict = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        # add the dictionary to the list of pizzas
        pizzas.append(pizza_dict)
    # create a response from the list of pizzas
    response = make_response(jsonify(pizzas), 200)
    return  response

@app.route('/pizza/<int:id>')   
def get_pizza(id):
    pizza = Pizza.query.filter_by(id=id).first()
    # if a pizza is not found, create an error message
    if pizza is None:
        # create a response with a 404 status code
        response = make_response(jsonify({'message': 'pizza not found'}),400)
        return response
    else:
        # create a dictionary to hold the information about the pizza
        pizza_dict = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        # create a response with a 200 status code
        response = make_response(jsonify(pizza_dict),200)
        return response

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    pizza_id = data['pizza_id']
    restaurant_id = data['restaurant_id']
    price = data['price']

    if price < 1 or price > 30:
        # if price is not between 1 and 30, return an error response
        return make_response(
            jsonify({'errors': ['validation errors']}),400)
    # create a new RestaurantPizza instance from the request's data
    new_restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id, restaurant_id=restaurant_id, price=price)
    # add the new RestaurantPizza to the database
    db.session.add(new_restaurant_pizza)
    # commit the new RestaurantPizza to the database
    db.session.commit()
    # return a response with the new RestaurantPizza's information
    return make_response(jsonify(new_restaurant_pizza.to_dict()),201)

@app.route('/restaurants/<int:id>', methods=['DELETE'])   
def delete_restaurant(id):
    # query the database for the restaurant with the given ID
    restaurant = Restaurant.query.filter_by(id=id).first()
    # if the restaurant does not exist, create a response with a 404 status code
    if restaurant is None:
        # create the response
        response = make_response(
            jsonify({'error': '["Restaurant not found"]'}), 404)
        return response
        
    # if the restaurant exists, delete it from the database
    db.session.delete(restaurant)
    # commit the changes to the database
    db.session.commit()
    # create a response with a 204 status code
    response = make_response(
        jsonify({'message': 'Restaurant deleted successfully'}), 204)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
