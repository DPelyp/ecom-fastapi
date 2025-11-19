# app/product.py
from decimal import Decimal

class Product:
    def __init__(self, id, sku, name, price, stock_qty):
        self._id = id
        self._sku = sku
        self._name = name
        self._price = Decimal(price)
        self._stock_qty = stock_qty

    # ---------- GETTERS ----------
    @property
    def id(self):
        return self._id

    @property
    def sku(self):
        return self._sku

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        if not v or not v.strip():
            raise ValueError("Назва товару не може бути пустою")
        self._name = v

    @property
    def price(self):
        return self._price
    
    # ---------- SETTERS ----------
    @price.setter
    def price(self, v):
        v = Decimal(v)
        if v < 0:
            raise ValueError("Ціна не може бути мінусовою")
        self._price = v

    @property
    def stock_qty(self):
        return self._stock_qty

    @stock_qty.setter
    def stock_qty(self, qty):
        qty = int(qty)
        if qty < 0:
            raise ValueError("Кількість не може бути мінусовою")
        self._stock_qty = qty

    # ---------- LOGIC ----------
    def final_price(self):
        return self.price
    
    @property
    def has_discount(self) -> bool:
        return False

    @property
    def discount_percent(self) -> int:
        return 0
    
    def can_reserve(self, qty: int) -> bool:
        qty = int(qty)
        return qty > 0 and self._stock_qty >= qty

    def __repr__(self):
        return (
            f"Product(id={self._id}, sku='{self._sku}', "
            f"name='{self._name}', price={self._price} грн, stock={self._stock_qty})"
        )