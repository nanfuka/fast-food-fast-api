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
    def user_login(self):
        cursor.execute("SELECT * FROM users WHERE username = '{}' and password = '{}'").format(self.username, self.password)    
        cursor.fetchone()

    def get_token(self):
        token = jwt.encode({'email': self.email}, 'secret', algorithm='HS256')
        return token    

    