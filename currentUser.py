import copy

from user import User
import shelve


class CurrentUser(User):
    def __init__(self, user: User):
        c = copy.deepcopy(user)
        super().__init__(c.email, c.password)

    def update(self):
        with shelve.open('users') as usersDB:
            usersDB[self.email] = self