import copy

from user import User
import shelve


class CurrentUser(User):
    def __init__(self, user: User):
        c = copy.deepcopy(user)
        super().__init__(c.email, c.password)
    @staticmethod
    def fromEmail(email):
        with shelve.open('users') as usersDB:
            return usersDB[email]
    def update(self):
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self