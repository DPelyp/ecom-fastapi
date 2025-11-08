# app/cart_runtime.py
from uuid import uuid4
from typing import Dict
from .catalog_seed import seed_catalog
from .goodsCategories import GoodsCategories

# Глобальний каталог (твій seed)
CATALOG: GoodsCategories = seed_catalog()

# Тут лежать усі кошики по сесіях (cookie cid)
_CARTS: Dict[str, "ShoppingCart"] = {}

# Твій клас кошика (копни як є або імпортуй звідти, де він у тебе лежить)
from decimal import Decimal

def as_dict(catalog) -> dict[int, dict]:
    result = {}
    for cat, products in catalog.categories.items():
        for p in products:
            result[p.id] = {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "category": cat,
                "price": p.price,
                "stock": p.stock_qty
            }
    return result

class ShoppingCart:
    def __init__(self, catalog: GoodsCategories):
        self.catalog = catalog
        self.items: dict[int, int] = {}

    def _find_product(self, product_id: int):
        for products in self.catalog.categories.values():
            for p in products:
                if p.id == product_id:
                    return p
        return None

def add_item(self, product_id: int, qty: int = 1):
    if qty <= 0:
        raise ValueError("qty must be positive")

    p = self._find_product(product_id)
    if p is None:
        raise KeyError(f"Product {product_id} not found in catalog")

    if getattr(p, "stock_qty", 0) < qty:
        raise ValueError("Not enough stock")

    p.stock_qty -= qty
    self.items[product_id] = self.items.get(product_id, 0) + qty

    # ⬇️ ось це нове
    return {"id": product_id, "name": p.name, "qty": qty}


    def remove_item(self, product_id: int, qty: int | None = None):
        if product_id not in self.items:
            return
        current = self.items[product_id]
        remove_qty = current if qty is None else min(qty, current)
        p = self._find_product(product_id)
        if p:
            p.stock_qty += remove_qty
        if remove_qty >= current:
            del self.items[product_id]
        else:
            self.items[product_id] = current - remove_qty

    def calculate_total(self) -> float:
        total = Decimal(0)
        for pid, qty in self.items.items():
            p = self._find_product(pid)
            if p is None:
                continue
            price = p.price if isinstance(p.price, Decimal) else Decimal(str(p.price))
            total += price * qty
        return float(total)

    def count(self) -> int:
        return sum(self.items.values())

def get_or_create_cid(request) -> str:
    cid = request.cookies.get("cid")
    if not cid:
        cid = uuid4().hex
    if cid not in _CARTS:
        _CARTS[cid] = ShoppingCart(CATALOG)
    return cid

def get_cart(cid: str) -> ShoppingCart:
    return _CARTS[cid]

def catalog_snapshot():
    return as_dict(CATALOG)