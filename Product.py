import datetime
import shelve


class Product:
    with shelve.open('products') as db:
        count = len(db)
    valid_categories = ['Fruits', 'Beverages', 'Vegetables', 'Meats' , 'Canned Food', 'Local', 'Discounted']
    def __init__(self, name: str, price: float, quantity: int, categories: [str], imageUrl: str, description: str ,expiry: datetime, weight: int):
        self.id = str(Product.count)
        Product.count += 1
        self.name = name
        self.price = price
        self.quantity = quantity
        self.categories = categories
        self.imageUrl = imageUrl
        self.description = description
        self.expiry = expiry.strftime("%d/%m/%Y")
        self.weight = weight
        with shelve.open("products") as products:
            products[self.id] = self
            Product.count = len(products)

    @staticmethod
    def remove_product(id):
        with shelve.open("products") as products:
            del products[id]
    @staticmethod
    def add_quantity(id, increment):
        with shelve.open("products") as products:
            p = products[id]
            p.quantity += increment
            products[id] = p
    @staticmethod
    def remove_quantity(id , increment):
        with shelve.open("products") as products:
            p = products[id]
            p.quantity -= increment
            products[id] = p
    @staticmethod
    def change_price(id, new_price):
        with shelve.open("products") as products:
            p = products[id]
            p.price = new_price
            products[id] = p
    @staticmethod
    def change_categories(id, categories):
        with shelve.open("products") as products:
            p = products[id]
            p.categories = categories
            products[id] = p
    @staticmethod
    def change_name(id,name):
        with shelve.open("products") as products:
            p = products[id]
            p.name = name
            products[id] = p

    @staticmethod
    def update_expiry(id, expiry: datetime):
        with shelve.open("products") as products:
            p = products[id]
            p.expiry = expiry.strftime("%d/%m/%Y")
            products[id] = p
#