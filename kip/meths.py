import psycopg2

connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
cursor = connection.cursor()

def sign_up(first_name, last_name, email, username, password, is_admin):        
    cursor.execute("INSERT INTO users(first_name, last_name, email, username, password, is_admin) VALUES('{}', '{}','{}','{}','{}','{}')".format(
    first_name, last_name, email, username, password, is_admin))
    connection.commit() 

def user_login(username, password):
    cursor.execute("SELECT username FROM users WHERE password = '{}'").format(password)    
    # cursor.execute("SELECT * FROM users WHERE password = '{}' and username = '{}'".format(password, username)) 
    connection.commit()
    user = cursor.fetchone()
    if user == username:
        return 'login successful'
    return 'wrong username and password'
    




def test_username(username):
    # cursor.execute("SELECT username FROM users WHERE password = '{}'").format(password)    
    cursor.execute("SELECT username FROM users WHERE password = '{}' and username = '{}'".format(password, username)) 
    connection.commit()

   
    

#     cursor.commit()
#     cursor.fetchone()

def get_dictionary(first_name, last_name, email, username,password):
    return{
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'username': username
        } 



def post_order(menu_id, user_id, quantity):
        cursor.execute("INSERT INTO orders(menu_id, user_id, quantity) VALUES('{}', '{}','{}')".format(
        menu_id, user_id, quantity))
        cursor.commit() 

def get_all_order():
        cursor.execute("SELECT * from orders")
        connection.commit()
        orders = cursor.fetchall()
        cursor.commit()
        return orders

def get_specific_order(order_id):
        cursor.execute("SELECT * from orders where order_id = '{}'" .format(order_id))
        orders = cursor.fetchone()
        cursor.commit()

def get_token(self):
    token = jwt.encode({'email': self.email}, 'secret', algorithm='HS256')
    return token

    # def update_order_request(self):
    #     cursor.execute("UPDATE orders SET menu_name = '{}' and price = '{}'".format(self.menu_name, self.price))WHERE
    #     menu_id IS '{}'" .format(self.menu_id);)
    #     cursor.commit()


def get_menu(self):
    cursor.execute("SELECT * from menu")
    cursor.commit()
    menu = cursor.fetchall()
def post_menu(menu_name, price):
    cursor.execute("INSERT INTO menu(menu_name, price) VALUES('{}','{}')".format(
    menu_name, price))
    cursor.commit()






    



