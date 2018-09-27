from werkzeug.security import safe_str_cmp
import jwt
import datetime
from flask import jsonify
from api.model.Responses import *
from functools import wraps
from flask import request


class DataStore:

    def __init__(self, users=[], orders=[]):

        self.users = users

        self.orders = orders
        self.key = "my Jesus I love thee"

    def create_user(self, user):
        """
        function to create a new user and append
        new user to the list of users
        """
        self.users.append(user)
        return user

    def add_orders(self, req):
        """
        function for placing a new order.
        this appends the newly placed order to the list of orders
        """
        self.orders.append(req)
        return req

    def get_all_orders(self):
        """function to return all orders"""
        return self.orders

    def get_all_orders_for_user(self, order):
        """function to return all orders for a specific user"""
        response = []
        for req in self.orders:
            if req.get_owner() == order:
                response.append(req.get_dictionary())
        return response

    def get_a_specific_requests_for_user(self, request_Id):
        """
        function to get a specific order for a specific user
        """
        for req in self.orders:
            if req.get_order_Id() == request_Id:
                return req.get_dictionary()
        return None

    def get_a_specific_order_for_user(self, request_Id):
        for req in self.orders:
            if req.get_order_Id() == request_Id:
                return req.get_dictionary()
        return None

    def update_order(self, order):
        """function to update an order"""
        i = 0
        for req in self.orders:
            if req.get_order_Id() == order.get_order_Id():
                self.orders[i] = order
                return order.get_dictionary()
            i = i+1
        return None

    def search_list(self, username):
        """function to search a list of users for a specific username"""
        for item in self.users:
            if item.get_username() == username:
                return item
            else:
                return None

    def generate_auth_token(self, user):
        """function to generate an auth-token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow(

                ) + datetime.timedelta(minutes=2000),
                'iat': datetime.datetime.utcnow(),
                'user': user
            }
            return jwt.encode(
                payload,
                self.key,
                algorithm='HS256'
            ).decode('utf-8')
        except Exception as e:
            return e

    def token_required(self, func):

        @wraps(func)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers['Authorization']
            else:
                return jsonify(auth_fail), 401
            try:
                data = jwt.decode(token, self.key)
                current_user = self.search_list(data['user']['username'])
            except:
                return jsonify(auth_fail), 401
            return func(current_user, *args, **kwargs)
        return decorated
