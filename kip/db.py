from pprint import pprint
import psycopg2 
 
   
connection = psycopg2.connect(host='localhost', user='postgres', password= 'test', database= 'fastfood')
cursor = connection.cursor()
cursor.execute("SELECT password FROM users WHERE username = '{}'".format(username))
r = cursor.fetchone()
pprint(r)