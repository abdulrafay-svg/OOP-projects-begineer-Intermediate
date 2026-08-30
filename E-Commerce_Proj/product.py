from exceptions import OutOfStockError

class Product:
    def __init__(self,product):  
        self.ID = product["id"]
        self.title = product["title"]
        self.stock = product["stock"]
        self.price = product["price"]

    def reduce_stock(self,quantity):
        if quantity > self.stock:
            raise OutOfStockError (f"Only {self.stock} left, requested {quantity}")
        self.stock -= quantity
    


