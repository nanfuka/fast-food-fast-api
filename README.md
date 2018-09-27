# fast-food-fast-api
[![Build Status](https://www.travis-ci.com/nanfuka/fast-food-fast-api.svg?branch=feature)](https://www.travis-ci.com/nanfuka/fast-food-fast-api)
[![Coverage Status](https://coveralls.io/repos/github/nanfuka/fast-food-fast-api/badge.svg?branch=feature)](https://coveralls.io/github/nanfuka/fast-food-fast-api?branch=feature)


# description
Fast-food-fast is a food delivery service app for a restaurant that facilitates  interaction between the restaurant users and administrator. The users should be able to  to reach out to the restaurant and make their food orders. they should also should be able to see a history of ordered foods.    The admin should be able to add, edit or delete the fast-food and  view the list of fast-food items. The administrator should also be able to view a list of orders, accept, decline orders or Mark orders as complete

## Project Features
* Users can create an account and log in
* A user should be able to order for food
* admin should be able to add,edit or delete the fast-food items
* The admin should be able to see a list of fast-food items
* The Admin user should be able to do the following:
    -See a list of orders
    -Accept and decline orders
    -Mark orders as completed
*A user should be able to see a history of ordered food

 

### API End Points Version 1

Endpoint | Functionality| Access
------------ | ------------- | -------------
GET /api/v1/orders | Get all the orders. | PRIVATE
GET /api/v1/orders/<orderId> | Fetch a specific order | PRIVATE
POST /api/v1/orders | Place a new order| PRIVATE
PUT /api/v1/orders/<orderId> | Update the status of an order. | PRIVATE
POST /api/v1/login | Logs in a User | PUBLIC

## Tests
The Project has been tested on
* TravisCI

## Heroku 
Go to [Debbie's fastfoodfast](https://debbiefastfood.herokuapp.com/)

## Instalation

Clone the GitHub repo:
 
` git clone https://github.com/nanfuka/fast-food-fast-api.git`

cd into the folder and install a Virtual Environment

` virtualenv venv`

Activate the virtual environment

`venv\scripts\activate`

Install all application requirements from the requirements file found in the root folder

`$ pip install -r requirements.txt`

Start Server 

`python app.py`.


## Contributors
* Deborah nanfuka

## How to Contribute
1. Download and install Git
2. Clone the repo `git clone https://github.com/nanfuka/fast-food-fast-api.git`
