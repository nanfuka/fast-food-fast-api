import psycopg2
class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database = 'foodlove', user = 'postgres', password = 'test')
                # database='d31g1i61q5vmq1', user='jadudvzdelgbad', password='18f22c2487a6c72e57257302dcf9ecab2b61f9d339bd4523cdcfb8878a2ffb6d', host='ec2-54-225-68-133.compute-1.amazonaws.com', port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except:
            print("Failed to connect to the database")

    def create_table_users(self):
        create_database_table = " CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, name  VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, username VARCHAR(50) NOT NULL UNIQUE, password VARCHAR(100) NOT NULL, create_date TIMESTAMP DEFAULT  CURRENT_TIMESTAMP, is_admin BOOLEAN)"
        self.cursor.execute(create_database_table)

    def create_table_menu(self):
        create_database_table = " CREATE TABLE IF NOT EXISTS menu(menu_id SERIAL PRIMARY KEY, menu_name  VARCHAR(100) NOT NULL UNIQUE, price INT NOT NULL UNIQUE)"
        self.cursor.execute(create_database_table)

    def create_table_orders(self):
        create_database_table = " CREATE TABLE IF NOT EXISTS orders(order_id SERIAL PRIMARY KEY, menu_id int NOT NULL, id int NOT NULL, quantity int NOT NULL, Order_status  VARCHAR(255), FOREIGN KEY (menu_id) REFERENCES menu(menu_id), FOREIGN KEY (id) REFERENCES users(id))"
        self.cursor.execute(create_database_table)

    def close(self):
        self.cursor.close()


if __name__ == "__main__":
    database_connection = DatabaseConnection()
    database_connection.create_table_users()
    database_connection.create_table_menu()
    database_connection.create_table_orders()
  
    # database_connection.delete_table()
