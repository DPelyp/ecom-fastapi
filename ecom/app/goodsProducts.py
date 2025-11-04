# app/product.py
from decimal import Decimal

class Product:
    def __init__(self, pid: int, sku: str, name: str, price, stock_qty: int):
        self.id = pid
        self.sku = sku
        self.name = name
        # одна валюта (гривня), просто гарантуємо точність
        self.price = Decimal(str(price))
        self.stock_qty = int(stock_qty)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price} грн, stock={self.stock_qty})"

    # на майбутнє (коли буде кошик):
    def can_reserve(self, qty: int) -> bool:
        return qty > 0 and self.stock_qty >= qty
