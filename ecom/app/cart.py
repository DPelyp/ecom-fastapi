from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation
from typing import Dict, Iterable, List, Optional, Union
from goodsCategories import GoodsCategories
from goodsProducts import Product

def _to_decimal(value) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"Invalid monetary value: {value!r}")

@dataclass
class CartItem:
    product_id: Union[int, str]
    name: str
    price: Decimal
    quantity: int = 1

    def subtotal(self) -> Decimal:
        return self.price * self.quantity

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["price"] = str(self.price)
        d["subtotal"] = str(self.subtotal())
        return d

class Cart:
    """Simple in-memory shopping cart for Product objects."""

    def __init__(self) -> None:
        self._items: Dict[Union[int, str], CartItem] = {}

    def _extract_product(self, product) -> (Union[int, str], str, Decimal): # type: ignore
        """Accept Product instance or dict-like object."""
        if isinstance(product, Product):
            pid = product.id
            name = product.name
            price = product.price
        elif isinstance(product, dict):
            pid = product.get("id") or product.get("pk")
            name = product.get("name") or product.get("title") or str(pid)
            price = product.get("price")
        else:
            # object with attributes
            pid = getattr(product, "id", None) or getattr(product, "pk", None)
            name = getattr(product, "name", None) or getattr(product, "title", None) or str(pid)
            price = getattr(product, "price", None)

        if pid is None or price is None:
            raise ValueError("Product must have 'id' and 'price'.")

        return pid, name, _to_decimal(price)

    def add(self, product, quantity: int = 1) -> CartItem:
        pid, name, price = self._extract_product(product)
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if pid in self._items:
            self._items[pid].quantity += quantity
        else:
            self._items[pid] = CartItem(product_id=pid, name=name, price=price, quantity=quantity)
        return self._items[pid]

    def remove(self, product_id: Union[int, str]) -> Optional[CartItem]:
        return self._items.pop(product_id, None)

    def update(self, product_id: Union[int, str], quantity: int) -> Optional[CartItem]:
        item = self._items.get(product_id)
        if item is None:
            return None
        if quantity <= 0:
            self.remove(product_id)
            return None
        item.quantity = quantity
        return item

    def get(self, product_id: Union[int, str]) -> Optional[CartItem]:
        return self._items.get(product_id)

    def contains(self, product_id: Union[int, str]) -> bool:
        return product_id in self._items

    def items(self) -> List[CartItem]:
        return list(self._items.values())

    def total(self) -> Decimal:
        return sum((item.subtotal() for item in self._items.values()), Decimal("0"))

    def count_items(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def clear(self) -> None:
        self._items.clear()

    def as_dict(self) -> Dict:
        return {
            "items": [item.to_dict() for item in self.items()],
            "total": str(self.total()),
            "count": self.count_items(),
        }

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterable[CartItem]:
        return iter(self._items.values())

    def __repr__(self) -> str:
        return f"<Cart items={len(self._items)} total={self.total()}>"