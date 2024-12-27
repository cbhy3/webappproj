import json

import bcrypt
from random import randint
import shelve

class User:
    password: str
    onlineStatus: bool
    email : str
    userCount = 0
    def __init__(self, email,password):
        self.email = email
        self.password = self.encryptPassword(password)
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
        self.userCount += 1

    def setPassword(self, password):
        self.password = self.encryptPassword(password)
    def setEmail(self, email):
        self.email = email
    def getEmail(self):
        return self.email
    def __str__(self):
        return f"{self.email}, {self.password}"
    ## Password encryption
    def encryptPassword(self,password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash.decode('utf-8')
    def verifyUser(self,plainPassword):
        return bcrypt.checkpw(plainPassword.encode('utf-8'), self.password.encode('utf-8'))

    def comparePassword(plainPassword, encryptedPassword):
        return bcrypt.checkpw(plainPassword.encode('utf-8'), encryptedPassword.encode('utf-8'))
    ##
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
    @staticmethod
    def fromJSON(jsonString):
        data = json.loads(jsonString)
        return User(**data)