from flask import Flask, request, jsonify, make_response
from model.methods import User
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return 'WELCOME TO FAST FOOD CHALLENGE 3'

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():

    user_data = request.get_json()
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    email = user_data.get('email')
    username = user_data.get('username')
    password = user_data.get('password')
    is_admin = user_data.get('is_admin')
    print(is_admin)

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
        
    print(is_admin)
    user = User(first_name, last_name, email, username, password, is_admin)
    user.add_user()

    return jsonify({"message": f"User {first_name} successfully created an account"}), 201


if __name__ == '__main__':
    app.run()