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





if __name__ == '__main__':
    app.run()
