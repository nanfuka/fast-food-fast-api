from flask import Flask, jsonify, request
from api.model.Responses import registration_successful, \
    login_fail, request_fail, create_request_successful, create_request_fail
from api.model.User import User
from api.model.orderRequest import OrderRequest
from api.model.data import DataStore


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






if __name__ == '__main__':
    app.run()
