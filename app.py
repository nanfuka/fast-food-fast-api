from flask import Flask, request, jsonify, make_response
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import psycopg2


app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return 'WELCOME TO FAST FOOD CHALLENGE 3'

@app.route('/api/v1/signup', methods=['POST'])
def register_user():

    user_data = request.get_json()
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')
    is_admin = user_data.get('is_admin')
    

    if user_data:
        print(user_data)
    if not user_data:
        return jsonify({'message': 'All fields are required'}), 400

    if not first_name or first_name == " ":
        return jsonify({'message': 'Invalid first_name'}), 400

    if not last_name or last_name == " ":
        return jsonify({'message': 'Invalid last_name'}), 400

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return make_response(jsonify({
            "status": "Fail",
            "message": "Enter valid email"}), 400)

    if not username or username == " " or username == type(int):
        return jsonify({'message': 'Invalid username'}), 400

    if not password or password == " " or len(password) < 5:
        return jsonify({'message': 'A stronger password  is required'}), 400
        
    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(first_name, last_name, email, username, password, is_admin) VALUES('{}','{}','{}','{}','{}','{}')".format(
        first_name, last_name, email, username, password, is_admin))
    connection.commit()

    return jsonify({"message": f"User {username} successfully created an account"}), 201

@app.route('/api/v1/auth/signin', methods=['POST'])
def signin_user():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("SELECT password, username FROM users WHERE password = '{}'".format(password))
    rows = cursor.fetchall()
    r = []
    for row in rows:
        user = {"user_id": row[0], "first_name":row[1], "last_name":row[2], "email": row[3], "username" : row[4], "password": row[5], "is_admin" : row[6]}
        r.append(user)
    for user in r:
        if user["username"]==username and user["password"]==password:
            return 'logged in'
        return 'not logged in'
        
@app.route('/api/v1/orders', methods=['POST'])
def api_create_orders():
    """api end point for placing a new order"""
    data = request.get_json(force=True)

    menu_id = data.get('menu_id', None)
    user_id = data.get('user_id', None)
    quantity = data.get('quantity', None)


    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO orders(menu_id, user_id, quantity)VALUES('{}','{}','{}')".format(
        menu_id, user_id, quantity))
    connection.commit()
    # cursor.execute("INSERT INTO orders(menu_id, user_id, quantity) VALUES('{}', '{}','{}')".format(
    #     menu_id, user_id, quantity))
    return 'order placed'

@app.route('/api/v1/orders', methods=['GET'])
def get_all_orders():
    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")
    users = cursor.fetchall()
    print (users)
    allusers =[]
    for row in users:
        user = {"order_id": row[0], "menu_id":row[1], "user_id":row[2], "quantity":row[3]}
        print(user)
        fine = allusers.append(user)
        print (fine)
        return jsonify(user)

@app.route('/api/v1/menu', methods=['POST'])
def create_menu():
    """api end point for creating menu"""
    data = request.get_json(force=True)

    menu_name = data.get('menu_name', None)
    price = data.get('price', None)

    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO menu(menu_name, price) VALUES('{}', '{}')".format(menu_name, price))
    connection.commit()
    return 'menu placed'


    



if __name__ == '__main__':
    app.run()