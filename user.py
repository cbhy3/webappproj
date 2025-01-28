import json

import bcrypt
from random import randint
import shelve

from Product import Product


class User:
    email : str
    Cart: {int : int}
    Codes: {str : int}
    Addresses: [str]
    Orders: [int]
    Cooldown: int
    def __init__(self, email,password):
        self.email = email
        self.password = self.encryptPassword(password)
        self.Addresses = []
        self.Cart = {}
        self.Orders = []
        self.Codes = {"TOTE" : 0 , "CHOC" : 0, "SHIP" : 0, "5OFF" : 0, "10OFF" : 0, "15OFF" : 0, "50OFF" : 0}
        self.Cooldown = 0 #in seconds
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


    def isAdmin(self):
        with shelve.open('admin') as adminDB:
            if self.email not in adminDB.keys():
                return False
            else:
                return True
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
    def clearCart(self):
        self.Cart.clear()
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
    def addCode(self, code):
        self.Codes[code] += 1
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self

    def removeCode(self, code):
        self.Codes[code] -= 1
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self

    def updateCooldown(self, newCooldown):
        self.Cooldown = newCooldown
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self

    def decreaseCooldown(self):
        self.Cooldown -= 1
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
    def addAddress(self, address):
        self.Addresses.append(address)
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
    def removeAddress(self, address):
        self.Addresses.pop(address)
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self
    def addAdmin(self):
        with shelve.open('admin') as adminsDB:
            adminsDB[self.email] = self
    def removeAdmin(self):
        with shelve.open('admin') as adminsDB:
            adminsDB.pop(self.email)