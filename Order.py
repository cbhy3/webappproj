import copy

from Product import Product
import shelve
import datetime
from generateOTP import updateOrderStatus

class Order:
    with shelve.open('Orders') as Orders:
        count = len(Orders)
    status = "Inactive"
    Products : { Product :int}

    def __init__(self, subtotal, cart, voucher, user, address):
        self.subtotal = subtotal
        self.voucher = voucher
        self.user = user
        self.Products = {}
        self.payment_method = None
        self.date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.datetime = datetime.datetime.now()
        self.address = address
        i = 0
        for products in cart:
            with shelve.open('products') as Products:
                if Products[str(products)].quantity >= cart[products]:
                    Product.add_quantity(str(products), -(cart[products]))
                    self.Products[i] = (cart[products],copy.deepcopy(Products[str(products)]))
                else:
                    print("not enough quantity")
                i+=1
        self.status = "PaymentPending"
        self.id = 0
        with shelve.open('Orders') as Orders:
            highest = 0
            for order in Orders:
                if Orders[order].id > highest:
                    highest = Orders[order].id
            self.id = highest + 1
            Orders[str(self.id)] = self
            print(f'Order created, id: {self.id}')
            Order.print_order(str(self.id))


    @staticmethod
    def updateStatus(id, status):
        with shelve.open('Orders') as Orders:
            order = Orders[id]
            order.status = status
            Orders[id] = order
            updateOrderStatus.sendEmail(order.user, order)
            print("email sent")
    @staticmethod
    def getStatus(id):
        with shelve.open('Orders') as Orders:
            order = Orders[id]
            return order.status
    @staticmethod
    def getUser(id):
        with shelve.open('Orders') as Orders:
            order = Orders[id]
            return order.user
    @staticmethod
    def print_order(id):
        with shelve.open('Orders') as Orders:
            for i in Orders[id].Products:
                for x in Orders[id].Products[i]:
                    print(x)
            print(Orders[id].voucher)
            print(Orders[id].user)
    @staticmethod
    def cancel_order(id):
        try:
            with shelve.open('Orders') as Orders:
                for i in Orders[id].Products:
                    Product.add_quantity( Orders[id].Products[i][1].id, Orders[id].Products[i][0])
                del Orders[id]
        except:
            print("order not found")
    @staticmethod
    def update_payment_method(id, payment_method):
        with shelve.open('Orders') as Orders:
            order = Orders[id]
            order.payment_method = payment_method
            Orders[id] = order

    def __str__(self):
        return f'{self.id}, {self.user}'