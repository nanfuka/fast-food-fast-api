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
    

if __name__ == '__main__':
    app.run()