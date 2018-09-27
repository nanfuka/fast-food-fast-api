from passlib.apps import custom_app_context as pwd_context


class User:
    def __init__(self, first_name, last_name, email,
                username, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_email(self, email):
        self.email = email

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def get_dictionary(self):
        return{
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username
        }

    def get_test_dictionary(self):
        return{
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
