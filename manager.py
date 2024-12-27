from admin import Admin
from customer import Customer

class Manager(Admin):
    def __init__(self,email,password):
        super().__init__(email,password)

    def addAdmin(self, customer: Customer):
        pass

    def removeAdmin(self, admin: Admin):
        pass

    def isManager(self):
        return True