from flask import Flask, jsonify, request
from api.model.responses import *
from api.model.user import User
from api.model.order_request import OrderRequest
from api.model.data import *
import jwt


app = Flask(__name__)

temp_orders = [OrderRequest("beef", "fresh", "36", "Deb"),  OrderRequest(
    "bacon", "fresh", "3", "Deb")]
temp_users = [User("Nsubuga", "Kalungiowak",
                   "llkldf@gmail.com", "Deb", "boosiko", True)]
data_store = DataStore(temp_users, temp_orders)


@app.route('/')
def api_documentation():
    return "WELCOME TO FAST FOOD FAST APPLICATION"


@app.route('/api/v1/login', methods=['POST'])
def login():
    """login"""

    data = request.get_json(force=True)
    username = data.get('username', None)
    password = data.get('password', None)

    user = data_store.search_list(username)
    if user is not None:
        if user.verify_password(password):
            response = user.get_dictionary()
            response["token"] = data_store.generate_auth_token(response)
            response["success"] = True
            print(str(response))
            return jsonify(response)
        else:
            return jsonify(login_fail), 200
    else:
        return jsonify(login_fail), 200


@app.route('/api/v1/register', methods=['POST'])
def register_user():
    """signup a new user"""
    data = request.args
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if first_name is not None and last_name is not None and \
            email is not None and username is not None and \
            password is not None:
        user = data_store.search_list(username)
        if user is None:
            response = data_store.create_user(
                User(
                    first_name, last_name, email, username, password)).\
                get_dictionary()
            response["token"] = data_store.generate_auth_token(response)
            registration_successful["user"] = response
            return jsonify(registration_successful)

        else:
            return jsonify(login_fail), 401
    else:
        return jsonify(create_request_fail)


@app.route('/api/v1/orders', methods=['POST'])
@data_store.token_required
def api_create_orders(current_user):
    """api end point for placing a new order"""
    data = request.get_json(force=True)

    food_order = data.get('food_order', None)
    description = data.get('description', None)
    quantity = data.get('quantity', None)

    if food_order is not None and description \
            is not None and quantity is not None:
        req = OrderRequest(food_order, description, quantity,
                           current_user.get_username())
        create_request_successful['data'] = data_store.add_orders(
            req).get_dictionary()
        return jsonify(create_request_successful)
    else:
        return jsonify(create_request_fail)


@app.route('/api/v1/orders', methods=['GET'])
@data_store.token_required
def get_all_orders(current_user):
    """function to retrieve all food orders"""

    return jsonify(data_store.get_all_orders_for_user(
        current_user.get_username()))


@app.route('/api/v1/orders/<order_Id>', methods=['GET'])
@data_store.token_required
def api_get_sepecific_order(current_user, order_Id):
    """this function fetches details
     about a specific order from the datastore"""
    req = data_store.get_a_specific_requests_for_user(order_Id)
    if req is not None:
        create_request_successful['data'] = req
        return jsonify(create_request_successful)
    else:
        return jsonify(request_fail)


@app.route('/api/v1/orders/<requestId>', methods=['PUT'])
@data_store.token_required
def api_modifys_request(current_user, requestId):
    """function to modify a specific order"""

    data = request.get_json(force=True)

    food_order = data.get('food_order', None)
    description = data.get('description', None)
    quantity = data.get('quantity', None)
    print(food_order)
    if food_order is not None and description \
            is not None and quantity is not None:
        req = OrderRequest(food_order, description, quantity,
                           current_user.get_username())
        mod_req = data_store.update_order(req)
        if mod_req is not None:
            create_request_successful['data'] = mod_req
            return jsonify(create_request_successful)
        else:
            return jsonify(request_fail)
    else:
        return jsonify(create_request_fail)

if __name__ == '__main__':
    app.run()
