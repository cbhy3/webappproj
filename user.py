import bcrypt
from random import randint

class User:
    userID: str
    password: str
    onlineStatus: bool
    email : str
    userCount = 0
    def __init__(self):
        self.userCount += 1
    def getUserID(self):
        return self.userID
    def setUserID(self, userID):
        self.userID = userID
    def setPassword(self, password):
        self.password = self.encryptPassword(password)
    def setEmail(self, email):
        self.email = email
    def getEmail(self):
        return self.email

    ## Password encryption
    def encryptPassword(self,password):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash.decode('utf-8')
    def verifyUser(self,plainPassword, hashedPassword):
        return bcrypt.checkpw(plainPassword.encode('utf-8'), hashedPassword.encode('utf-8'))
    ##
    def generateUID(self):
        pass  ## Need to add shelve first