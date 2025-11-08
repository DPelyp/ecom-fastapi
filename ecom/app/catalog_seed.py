from .goodsCategories import GoodsCategories
from .goodsProducts import Product
from decimal import Decimal


def seed_catalog() -> GoodsCategories:
        
    cats = GoodsCategories()
    cats.add_category("MMA")
    cats.add_category("Swimming")
    cats.add_category("Hiking")


    # --- MMA ---
    cats.add_product("MMA", Product(101, "SKU-001", "Рукавички MMA", 900.00, 10))
    cats.add_product("MMA", Product(102, "SKU-002", "Капа", 180.00, 50))
    cats.add_product("MMA", Product(103, "SKU-003", "Шолом боксерський Everlast", 1250.00, 7))
    cats.add_product("MMA", Product(104, "SKU-004", "Бинти еластичні RDX 4.5м", 250.00, 40))
    cats.add_product("MMA", Product(105, "SKU-005", "Мішок боксерський 30 кг", 2300.00, 4))
    cats.add_product("MMA", Product(106, "SKU-006", "Лапи тренувальні для спарингів", 720.00, 12))
    cats.add_product("MMA", Product(107, "SKU-007", "Кимоно для бойових мистецтв", 1800.00, 6))
    cats.add_product("MMA", Product(108, "SKU-008", "Щит для ударів (тайський пад)", 950.00, 9))
    cats.add_product("MMA", Product(109, "SKU-009", "Скакалка шкіряна", 280.00, 25))
    cats.add_product("MMA", Product(110, "SKU-010", "Захист паху чоловічий", 450.00, 18))

    # --- SWIMMING ---
    cats.add_product("Swimming", Product(201, "SKU-011", "Окуляри для плавання Arena", 350.00, 25))
    cats.add_product("Swimming", Product(202, "SKU-012", "Шапочка для плавання Speedo", 280.00, 30))
    cats.add_product("Swimming", Product(203, "SKU-013", "Ласти короткі для тренувань", 950.00, 15))
    cats.add_product("Swimming", Product(204, "SKU-014", "Дошка для плавання EVA", 520.00, 20))
    cats.add_product("Swimming", Product(205, "SKU-015", "Трубка для плавання фронтальна", 690.00, 12))
    cats.add_product("Swimming", Product(206, "SKU-016", "Плавки чоловічі Joss", 370.00, 30))
    cats.add_product("Swimming", Product(207, "SKU-017", "Купальник жіночий Arena", 780.00, 25))
    cats.add_product("Swimming", Product(208, "SKU-018", "Рушник мікрофібра 70×140", 310.00, 50))
    cats.add_product("Swimming", Product(209, "SKU-019", "Сумка для басейну 25L", 490.00, 18))
    cats.add_product("Swimming", Product(210, "SKU-020", "Плавальна дощечка дитяча", 290.00, 40))

    # --- HIKING ---
    cats.add_product("Hiking", Product(301, "SKU-021", "Рюкзак трекінговий 45L", 2100.00, 8))
    cats.add_product("Hiking", Product(302, "SKU-022", "Термос 1L", 480.00, 30))
    cats.add_product("Hiking", Product(303, "SKU-023", "Килимок каремат самонадувний", 1200.00, 10))
    cats.add_product("Hiking", Product(304, "SKU-024", "Пальник газовий туристичний", 850.00, 15))
    cats.add_product("Hiking", Product(305, "SKU-025", "Ліхтар налобний LED", 640.00, 22))
    cats.add_product("Hiking", Product(306, "SKU-026", "Термокружка 0.5L", 320.00, 35))
    cats.add_product("Hiking", Product(307, "SKU-027", "Трекінгові палиці 135см", 980.00, 16))
    cats.add_product("Hiking", Product(308, "SKU-028", "Кросівки трекінгові Salewa", 3450.00, 9))
    cats.add_product("Hiking", Product(309, "SKU-029", "Намет 2-місний Coleman", 5200.00, 5))
    cats.add_product("Hiking", Product(310, "SKU-030", "Павербанк 20 000 mAh з сонячною панеллю", 1150.00, 14))

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