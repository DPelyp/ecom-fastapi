# app/cart_runtime.py
from __future__ import annotations

from typing import Dict, Iterable, Tuple
from uuid import uuid4
from decimal import Decimal

from .catalog_seed import seed_catalog
from .goodsCategories import GoodsCategories

# Ініціалізуємо один спільний каталок (seed)
CATALOG: GoodsCategories = seed_catalog()


def _price_to_decimal(x) -> Decimal:
    """Нормалізуємо ціну до Decimal (без сюрпризів із float)."""
    if isinstance(x, Decimal):
        return x
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal("0")


class ShoppingCart:
    """
    Проста інмеморі-реалізація кошика, що знає:
    - про каталог (для пошуку продуктів та перевірки складу)
    - про свої позиції: items = {product_id: qty}
    """

    def __init__(self, catalog: GoodsCategories):
        self.catalog = catalog
        self.items: dict[int, int] = {}

    # ---------- внутрішнє ----------
    def _find_product(self, product_id: int):
        """Пошук продукту у всіх категоріях за id."""
        for products in self.catalog.categories.values():
            for p in products:
                if p.id == product_id:
                    return p
        return None

    # ---------- публічні методи ----------
    def add_item(self, product_id: int, qty: int = 1) -> dict:
        """Додає qty одиниць товару (зі зняттям зі складу)."""
        if qty <= 0:
            raise ValueError("qty must be positive")

        p = self._find_product(product_id)
        if p is None:
            raise KeyError(f"Product {product_id} not found in catalog")

        stock = int(getattr(p, "stock_qty", 0) or 0)
        if stock < qty:
            raise ValueError("Not enough stock")

        # оновлюємо склад і кошик
        setattr(p, "stock_qty", stock - qty)
        self.items[product_id] = self.items.get(product_id, 0) + qty

        return {"id": product_id, "name": getattr(p, "name", ""), "qty": qty}

    def remove_item(self, product_id: int, qty: int | None = None) -> int:
        """
        Зменшує кількість або прибирає позицію повністю.
        Повертає фактично зняту кількість (щоб, наприклад, повернути на склад).
        """
        if product_id not in self.items:
            return 0

        current = int(self.items[product_id])
        remove_qty = current if qty is None else max(0, min(int(qty), current))

        # повертаємо на склад
        p = self._find_product(product_id)
        if p is not None and remove_qty > 0:
            stock = int(getattr(p, "stock_qty", 0) or 0)
            setattr(p, "stock_qty", stock + remove_qty)

        # оновлюємо рядок
        left = current - remove_qty
        if left <= 0:
            self.items.pop(product_id, None)
        else:
            self.items[product_id] = left

        return remove_qty

    def set_qty(self, product_id: int, qty: int) -> None:
        """
        Жорстко виставляє кількість для позиції.
        Коректно докручує/зменшує склад.
        """
        if qty < 0:
            raise ValueError("qty must be >= 0")

        current = int(self.items.get(product_id, 0))

        if qty == current:
            return

        # якщо збільшуємо — перевіряємо склад
        if qty > current:
            delta = qty - current
            p = self._find_product(product_id)
            if p is None:
                raise KeyError(f"Product {product_id} not found in catalog")
            stock = int(getattr(p, "stock_qty", 0) or 0)
            if stock < delta:
                raise ValueError("Not enough stock")
            setattr(p, "stock_qty", stock - delta)
            self.items[product_id] = qty
        else:
            # зменшуємо — повертаємо на склад
            delta = current - qty
            p = self._find_product(product_id)
            if p is not None and delta > 0:
                stock = int(getattr(p, "stock_qty", 0) or 0)
                setattr(p, "stock_qty", stock + delta)

            if qty == 0:
                self.items.pop(product_id, None)
            else:
                self.items[product_id] = qty

    def clear(self) -> None:
        """Прибирає всі позиції (і повертає їх на склад)."""
        for pid, qty in list(self.items.items()):
            self.remove_item(pid, qty)
        self.items.clear()

    def count(self) -> int:
        """Загальна кількість одиниць у кошику."""
        return sum(int(q) for q in self.items.values())

    def calculate_total(self) -> float:
        """Сума кошика (грн)."""
        total = Decimal(0)
        for pid, qty in self.items.items():
            p = self._find_product(pid)
            if p is None:
                continue
            total += _price_to_decimal(getattr(p, "price", 0)) * int(qty)
        return float(total)

    def iter_items(self) -> Iterable[Tuple[object, int]]:
        """Ітератор по позиціях кошика: (Product, qty)."""
        for pid, qty in self.items.items():
            p = self._find_product(pid)
            if p is not None:
                yield p, int(qty)

class CartStore:
    """
    in-memory сховище кошиків по cid.
    """
    def __init__(self, catalog: GoodsCategories):
        self.catalog = catalog
        self._carts: Dict[str, ShoppingCart] = {}

    def get_or_create(self, cid: str) -> ShoppingCart:
        if cid not in self._carts:
            self._carts[cid] = ShoppingCart(self.catalog)
        return self._carts[cid]

    def get(self, cid: str) -> ShoppingCart:
        return self.get_or_create(cid)

_CART_STORE = CartStore(CATALOG)

def get_or_create_cid(request) -> str:
    """
    Дістає cid з cookie або генерує новий.
    Також гарантує наявність кошика у сховищі.
    """
    cid = request.cookies.get("cid")
    if not cid:
        cid = uuid4().hex
    _CART_STORE.get_or_create(cid)
    return cid


def get_cart(cid: str) -> ShoppingCart:
    return _CART_STORE.get(cid)

def as_dict(catalog) -> dict[int, dict]:
    result = {}
    for cat, products in catalog.categories.items():
        for p in products:
            result[p.id] = {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "category": cat,
                "price": getattr(p, "price", 0),
                "stock": getattr(p, "stock_qty", 0),
            }
    return result


def catalog_snapshot():
    return as_dict(CATALOG)