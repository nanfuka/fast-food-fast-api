import psycopg2


class DatabaseConnection:
    def __init__(self):
        
        self.connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()



class User(DatabaseConnection):

    def __init__(self, first_name, last_name, email, username, password):
        super().__init__()
       # self.first_name = first_name
        #self.last_name = last_name
        #self.email =  email
        #self.username = username
        #self.password = password  

    def add_user(self,  first_name, last_name, email, username, password, is_admin ):

        self.cursor.execute("INSERT INTO users(first_name, last_name, email, username, password) VALUES('{}', '{}','{}','{}','{}')".format(
        first_name, last_name, email, username, password))
        self.cursor.close()




