from flask import Flask, jsonify,request
from api.model.Responses import * 
from api.model.User import User
from api.model.UserRequest import UserRequest
from api.model.orderRequest import OrderRequest
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
    """
    login
    """

    data = request.get_json(force=True)
    username = data.get('username', None)
    password = data.get('password', None)

    user = data_store.searchList(username)
    if user is not None:
        if user.verify_password(password):
            response = user.getDictionary()
            response["token"] = data_store.generate_auth_token(response)
            response["success"] = True
            print(str(response))
            return jsonify(response)
        else:
            return jsonify(login_fail), 200
    else:
        return jsonify(login_fail), 200

# signup user


@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.args
    firstName = data.get("first_name")
    lastName = data.get("last_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if firstName is not None and lastName is not None and \
            email is not None and username is not None and \
            password is not None:
        user = data_store.searchList(username)
        if user is None:
            response = data_store.createUser(
                User(
                    firstName, lastName, email, username, password)).\
                    getDictionary()
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
    data = request.get_json(force=True)

    foodorder = data.get('foodorder', None)
    description = data.get('description', None)
    quantity = data.get('quantity', None)

    if foodorder is not None and description \
            is not None and quantity is not None:
        req = OrderRequest(foodorder, description, quantity,
                           current_user.getUserName())
        create_request_successful['data'] = data_store.addOrders(
            req).getDictionary()
        return jsonify(create_request_successful)
    else:
        return jsonify(create_request_fail)

# final get all orders


@app.route('/api/v1/orders', methods=['GET'])
@data_store.token_required
def place_new_order(current_user):
    return jsonify(data_store.getAllOrdersForUser(current_user.getUserName()))

# get specific order


@app.route('/api/v1/orders/<orderId>', methods=['GET'])
# get authorisation
@data_store.token_required
def api_gejt_sepecific_order(current_user, orderId):
    # fetch function from data.py Data class which return a particular order
    req = data_store.getASpecificRequestsForUser(orderId)
    # response if request is found
    if req is not None:
        create_request_successful['data'] = req
        return jsonify(create_request_successful)
    else:
        return jsonify(request_fail)

#Update the status of an order
@app.route('/api/v1/orders/<requestId>', methods=['PUT'])
@data_store.token_required
def api_modifys_request(current_user,requestId):
   
    data = request.get_json(force=True)

    foodorder = data.get('food order', None)
    description = data.get('description', None)
    quantity = data.get('quantity', None)
    print(foodorder)
#check all fields are filled
    if foodorder is not None and description  is not None and quantity  is not None:
        req = OrderRequest(foodorder,description,quantity,current_user.getUserName()) 
        mod_req=data_store.updateOrder(req)
        if mod_req is not None:
            create_request_successful['data'] = mod_req
            return jsonify(create_request_successful)
        else:
            return jsonify(request_fail)
    else:
        return jsonify(create_request_fail)








if __name__ == '__main__':
    app.run()
