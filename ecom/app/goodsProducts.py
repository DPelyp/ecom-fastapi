# app/product.py
from decimal import Decimal

class Product:
    def __init__(self, pid: int, sku: str, name: str, price, stock_qty: int,
                 image_url: str = "", description: str = ""):
        self.id = pid
        self.sku = sku
        self.name = name
        self.price = Decimal(str(price))
        self.stock_qty = int(stock_qty)
        self.image_url = image_url
        self.description = description

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price} грн, stock={self.stock_qty})"

    def can_reserve(self, qty: int) -> bool:
        return qty > 0 and self.stock_qty >= qty