from functools import wraps
from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():

    return jsonify('WELCOME TO FAST FOOD CHALLENGE 3') 

if __name__ == '__main__':
    app.run()