from flask import Flask, request, jsonify, make_response
import uuid
import re
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import psycopg2
from api.model.methods import User, Order, DatabaseConnection, Menu
from api import app


app = Flask(__name__)

def protected(f):
    """
    function for creating a decorator for the user. 
    it should be passed along with the header
    """
    @wraps(f)
    def decorated():
        auth = request.authorization
        if not auth:
            return jsonify({'message': 'Provide token'})
        else:
            try:
                jwt.decode(auth, 'secret', algorithms=['HS256'])
            except:              
                return jsonify({'message': 'Invalid token'})
        
    return decorated

@app.route('/', methods=['GET'])
def welcome():
    return 'WELCOME TO FAST FOOD CHALLENGE 3'

@app.route('/api/v1/signup', methods=['POST'])
def register_user():
    """
    function to register a new user with the food fast app.
    The user is required to enter their details as stupulated below
     """

    user_data = request.get_json()
    name = user_data.get('name')
    email = user_data.get('email')
    username = user_data.get('username')
    password = generate_password_hash(user_data.get('password'))
    is_admin = user_data.get('is_admin')

    if user_data:
        print(user_data)
    if not user_data:
        return jsonify({'message': 'All fields are required'}), 400

    if not name or name == " ":
        return jsonify({'message': 'Invalid name'}), 400

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        return make_response(jsonify({
            "status": "Fail",
            "message": "Enter valid email"}), 400)

    if not username or username == " " or username == type(int):
        return jsonify({'message': 'Invalid username'}), 400

    if not password or password == " " or len(password) < 5:
        return jsonify({'message': 'A stronger password  is required'}), 400

    user = User(name, email, username, password, is_admin)
    user.add_user()

    return jsonify({"message": "User successfully created an account"}) ,201
    
# @app.route('/api/v2/auth/login', methods=['POST'])
# def login():
#     """
#     function to log users into the database.
#     The user is required to input their username and password
#      """ 
#     connect = DatabaseConnection()
#     cursor = connect.cursor
    
#     login_data = request.get_json()
#     username = login_data['username']
#     password = generate_password_hash(login_data['password'])
  
#     cursor.execute(
#         "SELECT * FROM users WHERE username = '{}'".format(login_data['username']))
#     user = cursor.fetchone()

#     if cursor.fetchone():
#         user_token = User.get_token()
#         return jsonify({
#             'status': 'OK',
#             'message': f'Welcome {username} You are logged in',
#             'access_token': user_token.decode('utf8')
#             }), 200
#     else:
#         return jsonify({
#             'message': f'user {username} not found'
#         }), 404

#     user_data = request.get_json()
#     name = user_data.get('name')
#     email = user_data.get('email')
#     username = user_data.get('username')
#     password = generate_password_hash(user_data.get('password'))
#     is_admin = user_data.get('is_admin')

#     if user_data:
#         print(user_data)
#     if not user_data:
#         return jsonify({'message': 'All fields are required'}), 400

#     if not name or name == " ":
#         return jsonify({'message': 'Invalid name'}), 400

#     if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
#         return make_response(jsonify({
#             "status": "Fail",
#             "message": "Enter valid email"}), 400)

#     if not username or username == " " or username == type(int):
#         return jsonify({'message': 'Invalid username'}), 400

#     if not password or password == " " or len(password) < 5:
#         return jsonify({'message': 'A stronger password  is required'}), 400

#     user = User(name, email, username, password, is_admin)
#     return  user.add_user()

#     return jsonify({"message": f"User {name} successfully created an account"}) ,201
                     

@app.route('/api/v1/auth/login', methods=['POST'])
def logifdn():
    """
    function to log users into the database.
    The user is required to input their username and password
     """ 
    connect = DatabaseConnection()
    cursor = connect.cursor
    login_data = request.get_json()
    username = login_data['username']
    password = generate_password_hash(login_data['password'])
    if not username:
        return 'username  is required'
    if not username:
        return 'password  is required'
    cursor.execute(
        "SELECT * FROM users WHERE username = '{}'".format(login_data['username']))
    user = cursor.fetchone()

    if user:

        user_object = User(user[1], user[2], user[3], user[4])

        user_token = user_object.get_token()
        return jsonify({
            'status': 'OK',
            'message': f'Welcome {username} You are logged in',
            'access_token': user_token.decode('utf8')
            }), 200
    else:
        return jsonify({
            'message': f'user {username} not found'
        }), 404

   
@app.route('/api/v1/menu', methods=['POST'])
def create_menu():

    """api end point for creating menu"""
    data = request.get_json(force = True)
    menu_name = data.get('menu_name', None)
    price = data.get('price', None)
    
    if data:
        print(data)
    if not data:
        return jsonify({'message': 'All fields are required'}), 400
    if not menu_name:
        return jsonify({'message': 'All fields are required'}), 400

    if not price:
        return jsonify({'message': 'All fields are required'}), 400

    if isinstance(price, str):
        return jsonify({'message': 'Invalid menu'}), 400
        
    menu = Menu(menu_name, price)
    menu.create_menu()
    return jsonify({"message": "User successfully created an account"}) ,201
  


@app.route('/api/v1/menu', methods=['GET'])
@protected
def get_menu():
    """function to return all the orders placed"""
    cursor.execute("SELECT * FROM menu")
    men = cursor.fetchall()
    menu = []
    for row in men:
        menu.append({'menu_id' : row[0],
                    'menu_name' : row[1],
                    'price' :row[2]})
    return jsonify({"menu": menu}), 201

@app.route('/api/v1/orders', methods=['POST'])
def api_create_orders():

    """
    api end point for placing a new order
    and saving it to the database
     """
    data = request.get_json(force=True)

    menu_id = data.get('menu_id', None)
    id = data.get('id', None)
    order_status = data.get('order_status', None)
    quantity = data.get('quantity', None)

    if data:
        print(data)
    if not data:
        return jsonify({'message': 'All fields are required'}), 400

    if isinstance(id, str):
        return jsonify({'message': 'Invalid id'}), 400

    if isinstance(menu_id, str):
        return jsonify({'message': 'Invalid menu_id'}), 400
    
    if isinstance(quantity, str):
        return jsonify({'message': 'Invalid quantity'}), 400
    order = Order(menu_id, id, quantity, order_status)
    return order.create_order()
    return jsonify({"message": f"order has been placed successfully"}), 201

@app.route('/api/v1/orders/<int:user_id>', methods=['GET'])
def return_order_history_of_user(user_id):

    """function to return order history of a particular user"""
    connection = psycopg2.connect(host='localhost', user='postgres',
                                    password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", [user_id])
    orders = cursor.fetchall()
    print (orders)   
    all_orders = []
    for row in orders:
        all_orders.append({'order_id': row[0], 'menu_id': row[1],
                            'user_id': row[2], 'quantity': row[3]})
    return jsonify({"all_orders": all_orders}), 201

@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def return_one_order(order_id):

    """
    function to fetch a specific order. 
    The admin only inputs the order Id and 
    all teh details are displayed
    """
    connection = psycopg2.connect(host='localhost', user = 'postgres',
                                    password = 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = %s", [order_id])
   
    orders = cursor.fetchall()
    print (orders)   
    all_orders = []
    for row in orders:
        all_orders.append({'order_id': row[0], 'menu_id': row[1],
        'user_id' : row[2], 'quantity' : row[3]})
    return jsonify({"all_orders": all_orders}), 201

@app.route('/api/v1/menu/<int:order_id>', methods = ['PUT'])
@protected
def Update_order_status(order_status, order_id):
    """api end point for creating menu"""
    connection = psycopg2.connect(host='localhost',
    user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    command = "UPDATE orders SET order_status=%s WHERE order_id=%s"
    cursor.execute(commad(order_status, order_id))
        
    return jsonify({"user{}":'order has been modified'})
    
if __name__ == '__main__':
    app.run()