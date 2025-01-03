from user import User

class Customer(User):

    Cart: {str: [int, float]} ## cart will be a dictionary using the format {ItemName: [Quantity, Price]}
    Codes: [str] ## user's discount codes will be stored as a list of strings
    ShippingAddress: str
    def __init__(self,email,password):
        super().__init__(email,password)

    def addToCart(self, item, quantity, price):
        pass

    def removeFromCart(self, item, quantity):
        pass

    def checkOut(self):
        pass

    def redeemCode(self, code):
        if code in self.Codes:
            pass

