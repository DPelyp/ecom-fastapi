from .goodsCategories import GoodsCategories
from .goodsProducts import Product
from decimal import Decimal


def seed_catalog() -> GoodsCategories:
        
    cats = GoodsCategories()
    cats.add_category("MMA")
    cats.add_category("Swimming")
    cats.add_category("Hiking")
    cats.add_category("Cycling")


    # --- MMA ---
    cats.add_product("MMA", Product(101, "SKU-001", "Рукавички MMA", 900.00, 10))
    cats._by_id[101].image_url = "/static/mma/gloves.avif"
    cats._by_id[101].description = "Легкі рукавички MMA з щільною амортизацією та м’якою підкладкою. Вентиляційні отвори й надійна липучка для фіксації — ідеально для тренувань і спарингів."

    cats.add_product("MMA", Product(102, "SKU-002", "Капа", 180.00, 50))
    cats._by_id[102].image_url = "/static/mma/kapa.jpg"
    cats._by_id[102].description = "Двошарова термопластична капа, що формується у гарячій воді під вашу щелепу. Дає вільно дихати та постачається з футляром."

    cats.add_product("MMA", Product(103, "SKU-003", "Шолом боксерський Everlast", 1250.00, 7))
    cats._by_id[103].image_url = "/static/mma/helmet.webp"
    cats._by_id[103].description = "Шолом Everlast із багатошаровою піною та розширеним кутом огляду. Синтетична шкіра, посилені шви й зручні липучки для швидкої посадки."

    cats.add_product("MMA", Product(104, "SKU-004", "Бинти еластичні RDX 4.5м", 250.00, 40))
    cats._by_id[104].image_url = "/static/mma/binty.jpg"
    cats._by_id[104].description = "Еластичні бинти RDX 4.5 м з петелькою на великий палець та надійною липучкою. Дихаюча бавовна стабілізує зап’ястя й суглоби."

    cats.add_product("MMA", Product(105, "SKU-005", "Мішок боксерський 30 кг", 2300.00, 4))
    cats._by_id[105].image_url = "/static/mma/grusha.webp"
    cats._by_id[105].description = "Боксерський мішок 30 кг із міцної ПВХ-екошкіри, посилені шви та стальні ланцюги. Текстильне наповнення тримає форму — підходить для дому й залу."

    cats.add_product("MMA", Product(106, "SKU-006", "Лапи тренувальні для спарингів", 720.00, 12))
    cats._by_id[106].image_url = "/static/mma/lapy.jpg"
    cats._by_id[106].description = "Пара тренувальних лап із вигином під долоню та щільною амортизацією. Перфорація відводить тепло, кріплення фіксує руку під час серій."

    cats.add_product("MMA", Product(107, "SKU-007", "Кимоно для бойових мистецтв", 1800.00, 6))
    cats._by_id[107].image_url = "/static/mma/kimono.jpg"
    cats._by_id[107].description = "Кімоно для BJJ/джіу-джитсу зі щільної плетінки (≈350–450 gsm) та підсиленими швами. Зручний крій для партеру; пояс у комплект не входить."

    cats.add_product("MMA", Product(108, "SKU-008", "Щит для ударів (тайський пад)", 950.00, 9))
    cats._by_id[108].image_url = "/static/mma/shield.jpg"
    cats._by_id[108].description = "Тайський пад/щит із щільною піною та анатомічною кривизною для прийому ударів. Подвійні ручки і ремені забезпечують надійну фіксацію."   

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

    # --- CYCLING (Велоспорт) ---
    cats.add_product("Cycling", Product(401, "SKU-041", "Велосипедний шолом MTB", 1250.00, 18))
    cats.add_product("Cycling", Product(402, "SKU-042", "Рукавички велосипедні", 390.00, 40))
    cats.add_product("Cycling", Product(403, "SKU-043", "Фара передня 800 лм (USB)", 720.00, 26))
    cats.add_product("Cycling", Product(404, "SKU-044", "Ліхтар задній строб (USB)", 390.00, 34))
    cats.add_product("Cycling", Product(405, "SKU-045", "Насос підлоговий з манометром", 980.00, 15))
    cats.add_product("Cycling", Product(406, "SKU-046", "Сідло гелеве Comfort", 860.00, 20))
    cats.add_product("Cycling", Product(407, "SKU-047", "Ланцюг 11-швидк. KMC", 890.00, 28))
    cats.add_product("Cycling", Product(408, "SKU-048", "Камера 29\" x 2.10 (AV)", 210.00, 60))
    cats.add_product("Cycling", Product(409, "SKU-049", "Пляшка для води 750 мл", 190.00, 55))
    cats.add_product("Cycling", Product(410, "SKU-050", "Фляготримач алюмінієвий", 220.00, 45))
    cats.add_product("Cycling", Product(411, "SKU-051", "Велокомп'ютер бездротовий", 1350.00, 12))
    cats.add_product("Cycling", Product(412, "SKU-052", "Педалі контактні SPD", 1750.00, 14))

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

cart = ShoppingCart(catalog)
cart.add_item(101, 2)   # add 2 x product 101
cart.add_item(301, 1)   # add 1 x product 301
print("Total:", cart.calculate_total())
cart.remove_item(101, 1)  # remove 1 of product 101
print("Total after removal:", cart.calculate_total())
print("Cart items:", cart.items)
print("Catalog stock snapshot:", as_dict(catalog))