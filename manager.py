from admin import Admin
from customer import Customer

class Manager(Admin):
    def __init__(self):
        super().__init__()

    def addAdmin(self, customer: Customer):
        pass

    def removeAdmin(self, admin: Admin):
        pass