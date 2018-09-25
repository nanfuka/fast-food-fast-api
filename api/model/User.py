from passlib.apps import custom_app_context as pwd_context


class User:
    def __init__(self, firstName, lastName, email, username, password, is_admin=False):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName

    def getEmail(self):
        return self.email

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password

    def setFirstName(self, firstName):
        self.firstName = firstName

    def setLastName(self, lastName):
        self.lastName = lastName

    def setEmail(self, email):
        self.email = email

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def getDictionary(self):
        return{
            'first_name': self.firstName,
            'last_name': self.lastName,
            'email': self.email,
            'username': self.username
        }

    def getTestDictionary(self):
        return{
            'first_name': self.firstName,
            'last_name': self.lastName,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
