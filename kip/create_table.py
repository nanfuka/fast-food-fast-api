#!/usr/bin/python

import psycopg2

conn = psycopg2.connect(database="fastfood", user="postgres", password="test", host="127.0.0.1", port="5432")
print ("fastfood database created")

cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS users""")
cur.execute("""DROP TABLE IF EXISTS menu""")
cur.execute("""DROP TABLE IF EXISTS orders""")
cur.execute('''CREATE TABLE users
       (user_id SERIAL PRIMARY KEY,
       create_date TIMESTAMP DEFAULT  CURRENT_TIMESTAMP,
       first_name VARCHAR(100) NOT NULL,
       last_name VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL UNIQUE,
       username VARCHAR(100) NOT NULL UNIQUE,
       password VARCHAR(100) NOT NULL,
       is_admin VARCHAR(100) NOT NULL);''')
print ("user-Table created.")


cur.execute('''CREATE TABLE menu
       (menu_id SERIAL PRIMARY KEY,
       menu_name VARCHAR(100) NOT NULL,
       price VARCHAR(100) NOT NULL);''')
print ("menu-Table created.")


cur.execute('''ghg''')
print ("order-Table created.")


