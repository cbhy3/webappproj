import shelve

from user import User

class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        with shelve.open('admin') as db:
            db[self.email] = self

    ##add more functions for:
    ##checking orders
    ##updating items db
    ##responding to support tickets

    def isAdmin(self):
        return True