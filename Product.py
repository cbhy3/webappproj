import datetime
import shelve


class Product:
    with shelve.open('products') as db:
        count = len(db)
    valid_categories = ['Dairy', 'Bakery & Grains', 'Meat & Seafood', 'Pantry and Cooking Essentials', 'Snacks & Sweets', 'Beverages' , 'Frozen Foods', 'Fruits & Vegetables', 'Household & Cleaning Supplies', 'Locally Sourced', 'Canned Foods']
    def __init__(self, name: str, price: float, quantity: int, categories: [str], imageUrl: str, description: str ,expiry: datetime, weight: int):
        self.id = None
        while self.id is None:
            try:
                with shelve.open('products') as db:
                    db[str(Product.count)]
                Product.count += 1
            except KeyError:
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
            print(f'New quantity for product {id}: {p.quantity}')

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
    @staticmethod
    def change_description(id, description):
        with shelve.open("products") as products:
            p = products[id]
            p.description = description
            products[id] = p

    @staticmethod
    def change_weight(id, weight):
        with shelve.open("products") as products:
            p = products[id]
            p.weight = weight
            products[id] = p
    @staticmethod
    def change_image(id, imageUrl):
        with shelve.open("products") as products:
            p = products[id]
            p.imageUrl = imageUrl
            products[id] = p
    def __str__(self):
        return f'{self.name}, id: {self.id}'