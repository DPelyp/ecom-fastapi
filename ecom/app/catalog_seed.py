from .goodsCategories import GoodsCategories
from .goodsProducts import Product
from decimal import Decimal


def seed_catalog() -> GoodsCategories:
        
    cats = GoodsCategories()
    cats.add_category("MMA")
    cats.add_category("Swimming")
    cats.add_category("Hiking")


    cats.add_product("MMA", Product(101, "SKU-001", "Рукавички MMA", 900.00, 10))
    cats.add_product("MMA", Product(102, "SKU-002", "Капа", 180.00, 50))
    cats.add_product("Swimming", Product(201, "SKU-010", "Окуляри для плавання", 350.00, 25))
    cats.add_product("Swimming", Product(202, "SKU-010", "Шапочка для плавання", 350.00, 25))
    cats.add_product("Hiking", Product(301, "SKU-020", "Рюкзак трекінговий 45L", 2100.00, 8))
    cats.add_product("Hiking", Product(302, "SKU-021", "Термос 1L", 480.00, 30))


    return cats

catalog = seed_catalog()

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
        # items: mapping product_id -> qty
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
        # reserve stock
        p.stock_qty -= qty
        self.items[product_id] = self.items.get(product_id, 0) + qty

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

# example usage using the seeded catalog
cart = ShoppingCart(catalog)
cart.add_item(101, 2)   # add 2 x product 101
cart.add_item(301, 1)   # add 1 x product 301
print("Total:", cart.calculate_total())
cart.remove_item(101, 1)  # remove 1 of product 101
print("Total after removal:", cart.calculate_total())
print("Cart items:", cart.items)
print("Catalog stock snapshot:", as_dict(catalog))