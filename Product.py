import shelve


class Product:
    count = 0
    valid_categories = ['Fruits', 'Beverages', 'Vegetables', 'Meats' , 'Canned Food', 'Local', 'Discounted']
    def __init__(self, name: str, price: float, quantity: int, categories: [str], imageUrl: str, description: str):
        self.id = str(Product.count)
        Product.count += 1
        self.name = name
        self.price = price
        self.quantity = quantity
        self.categories = categories
        self.imageUrl = imageUrl
        self.description = description
        with shelve.open("products") as products:
            products[self.id] = self

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

with shelve.open("products") as products:
    for i in products:
        del products[i]
Product("nuts", 30.99, 6, ["Fruits"], "tetsicles", "just dance dududududud babab dudu jhust dance dababduda babadudud")
Product("balls", 50.99, 6, ["Fruits", "Beverage", "Discounted"], "tetsicles", "i wlka a lonely road the only one that i have ever kjnown dont know whereh it goes but its all on me and i wlak alone ")
Product("huge", 10.99, 6, ["Meats", "Local"], "tetsicles", "hey i just met y ou and thisis crazy so ehres my number call me maybe")