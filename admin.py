from user import User

class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)


    ##add more functions for:
    ##checking orders
    ##updating items db
    ##responding to support tickets

    