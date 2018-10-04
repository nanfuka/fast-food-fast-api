from flask import Flask, request, jsonify, make_response
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import psycopg2
from api.model.methods import *


app = Flask(__name__)

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify({'message': 'Provide token'})
        else:
            try:
                jwt.decode(auth, 'secret', algorithms=['HS256'])
            except Exception as e:
                print(e)
                return jsonify({'message': 'Invalid token'})
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def welcome():
    return 'WELCOME TO FAST FOOD CHALLENGE 3'
@app.route('/api/v1/signup', methods=['POST'])
def register_user():

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

    return jsonify({"message": f"User {name} successfully created an account"}), 201

@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    connect = DatabaseConnection()
    cursor = connect.cursor
    login_data = request.get_json()
    username = login_data['username']
    password = generate_password_hash(login_data['password'])
  
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


if __name__ == '__main__':
    app.run()