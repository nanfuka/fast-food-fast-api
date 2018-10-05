from tables import DatabaseConnection
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime



db_connect = DatabaseConnection()
connect = db_connect.connection
cursor = db_connect.connection.cursor()


class User(DatabaseConnection):

    def __init__(self, name, email, username, password, is_admin=False):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = is_admin


    def add_user(self):
        cursor.execute("INSERT INTO users(name, email, username, password, is_admin) VALUES('{}', '{}','{}','{}','{}')".format(
        self.name, self.email, self.username, self.password, self.is_admin))
        cursor.close()

    def get_token(self):
        token = jwt.encode({'email': self.email}, 'secret', algorithm='HS256')
        return token
    # def get_admin_token(self):
    #     token = jwt.encode({'email': self.email}, 'secret', algorithm='HS256')
    #     return token
        
    
class Menu(DatabaseConnection):

    def __init__(self, menu_name, price=int):
       
        self.menu_name = menu_name
        self.price = price

    def create_menu(self):
        cursor.execute("INSERT INTO menu(menu_name, price) VALUES('{}', '{}')".format(
        self.menu_name, self.price))
        cursor.close()

    def get_menu(self):
        cursor.execute("SELECT * FROM menu")
        cursor.close()

class Order(DatabaseConnection):

    def __init__(self, menu_id, id, quantity, order_status):
       
        self.menu_id = menu_id
        self.id = id
        self.quantity = quantity
        self.order_status = order_status

    def create_order(self):
        cursor.execute("INSERT INTO orders(menu_id, id, quantity, order_status) VALUES({}, {}, {}, '{}')".format(
        self.menu_id, self.id, self.quantity, self.order_status))
        cursor.close()

    def get_user_order_history(self, id):
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", [id])
        cursor.fetchall()
        cursor.close()


  

    