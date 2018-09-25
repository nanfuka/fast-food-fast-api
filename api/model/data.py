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

    def createUser(self, user):
        """
        function to create a new user and append new user to the list of users
        """
        self.users.append(user)
        return user

    def addOrders(self, req):
        """
        function for placing a new order.
        this appends the newly placed order to the list of orders
        """
        self.orders.append(req)
        return req

    def getAllOrders(self):
        """
        function to return all orders
        """
        return self.orders

    def getAllOrdersForUser(self, order):
        """
        function to return all orders for a specific user
        """
        response = []
        for req in self.orders:
            if req.getOwner() == order:
                response.append(req.getDictionary())
        return response

    def getASpecificRequestsForUser(self, requestId):
        """
        function to get a specific order for a specific user
        """
        for req in self.orders:
            if req.getOrderId() == requestId:
                return req.getDictionary()
        return None

    def getASpecificOrderForUser(self, requestId):
        for req in self.orders:
            if req.getOrderId() == requestId:
                return req.getDictionary()
        return None

    def updateOrder(self, order):
        """
        function to update an order
        """
        i = 0
        for req in self.orders:
            if req.getOrderId() == order.getOrderId():
                self.orders[i] = order
                return order.getDictionary()
            i = i+1
        return None

    def searchList(self, username):
        """
        function to search a list of users for a specific username
        """
        for item in self.users:
            if item.getUserName() == username:
                return item
            else:
                return None

    def generate_auth_token(self, user):
        """
        function to generate an auth-token
        """
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
                current_user = self.searchList(data['user']['username'])
            except:
                return jsonify(auth_fail), 401
            return func(current_user, *args, **kwargs)
        return decorated
