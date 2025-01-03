import json

import bcrypt
from random import randint
import shelve

class User:

    onlineStatus: bool
    email : str
    userCount = 0
    def __init__(self, email,password):
        self.email = email
        self.password = self.encryptPassword(password)
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
        self.userCount += 1
        self.id = User.userCount
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
    @staticmethod
    def comparePassword(plainPassword, encryptedPassword):
        return bcrypt.checkpw(plainPassword.encode('utf-8'), encryptedPassword.encode('utf-8'))
    ##
    @staticmethod

    def isAdmin(self):
        return False