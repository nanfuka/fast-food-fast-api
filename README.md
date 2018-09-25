# fast-food-fast-api
[![Build Status](https://www.travis-ci.com/nanfuka/fast-food-fast-api.svg?branch=feature)](https://www.travis-ci.com/nanfuka/fast-food-fast-api)
Fast-food-fast is a food delivery service app for a restaurant that facilitates  interaction between the restaurant users and administrator. The users should be able to  to reach out to the restaurant and make their food orders. they should also should be able to see a history of ordered foods.    The admin should be able to add, edit or delete the fast-food and  view the list of fast-food items. The administrator should also be able to view a list of orders, accept, decline orders or Mark orders as complete


Project Features

. Users can create an account and log in
. A user should be able to order for food
. admin should be able to add,edit or delete the fast-food items
. The admin should be able to see a list of fast-food items
. The Admin user should be able to do the following:
    -See a list of orders
    -Accept and decline orders
    -Mark orders as completed
.A user should be able to see a history of ordered food

##API end points

*GET /orders
 Get all the orders.
*GET /orders/<orderId>
Fetch a specific order
*POST /orders
Place a new order.
*PUT /orders/<orderId>
Update the status of an order.