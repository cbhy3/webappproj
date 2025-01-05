import json

import bcrypt
from random import randint
import shelve

from Product import Product


class User:

    email : str
    Cart: {int : int}
    Codes: [str]
    def __init__(self, email,password):
        self.email = email
        self.password = self.encryptPassword(password)
        self.Cart = {}
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self

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

    def addToCart(self, product):
        try:
            self.Cart.get(product)
            self.Cart.update({product: self.Cart[product] + 1})
        except KeyError as e:
            self.Cart[product] = 1
        finally:
            with shelve.open('users') as usersDB:
                 usersDB[self.email] = self

    def removeFromCart(self, product):
        if self.Cart.get(product) != 1:
            self.Cart.update({product: self.Cart[product] - 1})
        else:
            self.Cart.pop(product)
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self