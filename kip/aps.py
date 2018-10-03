
from flask import Flask, jsonify, request
from api.model.responses import *
from api.model.meths import *

import jwt
app = Flask(__name__)


@app.route('/')
def welcome():
    return 'hello'

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


@app.route('/api/v1/auth/signin', methods=['POST'])
def signin_user():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username = '{}'".format(username))
    r = cursor.fetchone()
    if r == password:
        return 
    return 'you have notlogged in'

    



# @app.route('/api/v1/orders', methods=['POST'])
# @data_store.token_required
# def api_create_orders(current_user):
#     """api end point for placing a new order"""
#     data = request.get_json(force=True)

#     food_order = data.get('food_order', None)
#     description = data.get('description', None)
#     quantity = data.get('quantity', None)

#     if food_order is not None and description \
#             is not None and quantity is not None:
#         req = OrderRequest(food_order, description, quantity,
#                            current_user.get_username())
#         create_request_successful['data'] = data_store.add_orders(
#             req).get_dictionary()
#         return jsonify(create_request_successful)
#     else:
#         return jsonify(create_request_fail)


# @app.route('/api/v1/orders', methods=['GET'])
# @data_store.token_required
# def get_all_orders(current_user):
#     """function to retrieve all food orders"""

#     return jsonify(data_store.get_all_orders_for_user(
#         current_user.get_username()))


# @app.route('/api/v1/orders/<order_Id>', methods=['GET'])
# @data_store.token_required
# def api_get_sepecific_order(current_user, order_Id):
#     """this function fetches details
#      about a specific order from the datastore"""
#     req = data_store.get_a_specific_requests_for_user(order_Id)
#     if req is not None:
#         create_request_successful['data'] = req
#         return jsonify(create_request_successful)
#     else:
#         return jsonify(request_fail)


# @app.route('/api/v1/orders/<requestId>', methods=['PUT'])
# @data_store.token_required
# def api_modifys_request(current_user, requestId):
#     """function to modify a specific order"""

#     data = request.get_json(force=True)

#     food_order = data.get('food_order', None)
#     description = data.get('description', None)
#     quantity = data.get('quantity', None)
#     print(food_order)
#     if food_order is not None and description \
#             is not None and quantity is not None:
#         req = OrderRequest(food_order, description, quantity,
#                            current_user.get_username())
#         mod_req = data_store.update_order(req)
#         if mod_req is not None:
#             create_request_successful['data'] = mod_req
#             return jsonify(create_request_successful)
#         else:
#             return jsonify(request_fail)
#     else:
#         return jsonify(create_request_fail)



# @app.route('/api/v1/auth/login', methods=['POST'])
# def register_user():
# @app.route('/api/v1/login', methods=['POST'])
# def login():
#     """login"""


#     data = request.get_json(force=True)
#     username = data.get('username', None)
#     password = data.get('password', None)


#     connection.commit()    
#     item = cursor.fetchone()
    

#     if item is not None:

       
#         # if usa.verify_password(password):

#         #     response = user.get_dictionary()
#         #     response["token"] = user.generate_auth_token(response)
#         #     response["success"] = True
#         #     print(str(response))
#         #     return jsonify(response)
#         # return jsonify({"user": item})
#     else:
#         return 'not loggedin'




@app.route('/api/v1/users/orders', methods=['POST'])
def place_orders():
    """api end point for placing a new order"""
    data = request.get_json(force=True)

    menu_id = data.get('menu_id', None)
    user_id = data.get('user_id', None)
    quantity = data.get('quantity', None)

    if menu_id is not None and user_id\
            is not None and quantity is not None:
        new_order = post_order(menu_id, user_id, quantity)
        return jsonify(create_request_successful)


# @app.route('/api/v1/orders/ ', methods=['GET'])
# def get_orders():
#     return jsonify ('orders':get_all_order())


# @app.route('/api/v1/orders/<orderId>', methods=['GET'])
# def return specific_order():
#     return jsonify (get_specific_order)

# # @app.route('/api/v1/orders/<orderId>', methods=['POST'])
# # def register_user():

# @app.route('/api/v1//menu', methods=['POST'])
# def register_user():
#         """api end point for placing a new order"""
#     data = request.get_json(force=True)


#     menu_name = data.get('menu_name', None)
#     price = data.get('price', None)

#     if menu_name is not None and price is not None:
#         new_menu = post_menu(menu_name, price)
#         return jsonify(added on menu sucessfully)

# @app.route('/api/v1/menu', methods=['GET'])
# def register_user():
if __name__ == '__main__':
    app.run()



