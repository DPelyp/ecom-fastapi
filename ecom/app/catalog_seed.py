from .goodsCategories import GoodsCategories
from .goodsProducts import Product
from decimal import Decimal
from .discountedProduct import DiscountedProduct


def seed_catalog() -> GoodsCategories:
        
    cats = GoodsCategories()
    cats.add_category("MMA")
    cats.add_category("Swimming")
    cats.add_category("Hiking")
    cats.add_category("Cycling")

    # --- MMA ---
    cats.add_product("MMA", DiscountedProduct(
    101, "SKU-001", "Рукавички MMA", 900.00, 10, discount=0.15))

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
    cats._by_id[201].image_url = "/static/swimming/glasses.webp"
    cats._by_id[201].description = "Окуляри для плавання Arena з антифогом і УФ-захистом. Регульований носовий міст і ремінець забезпечують комфортну посадку для різних форм обличчя."   

    cats.add_product("Swimming", Product(202, "SKU-012", "Шапочка для плавання Speedo", 280.00, 30))
    cats._by_id[202].image_url = "/static/swimming/shapochka.webp"
    cats._by_id[202].description = "Силіконова шапочка для плавання Speedo, що щільно прилягає та знижує опір води. М'який матеріал не тягне волосся і забезпечує комфорт під час тренувань."

    cats.add_product("Swimming", Product(203, "SKU-013", "Ласти короткі для тренувань", 950.00, 15))
    cats._by_id[203].image_url = "/static/swimming/lasty.jpg"
    cats._by_id[203].description = "Короткі ласти для плавання, що покращують техніку удару ногами. Гнучкий матеріал і ергономічний дизайн забезпечують комфорт і ефективність тренувань."

    cats.add_product("Swimming", Product(204, "SKU-014", "Дошка для плавання EVA", 520.00, 20))
    cats._by_id[204].image_url = "/static/swimming/doshka.jpg"
    cats._by_id[204].description = "Дошка для плавання з EVA-піни, що забезпечує плавучість і комфорт. Ідеальна для розвитку техніки рук і ніг під час тренувань у басейні."

    cats.add_product("Swimming", Product(205, "SKU-015", "Трубка для плавання фронтальна", 690.00, 12))
    cats._by_id[205].image_url = "/static/swimming/trybka.jpg"
    cats._by_id[205].description = "Фронтальна трубка для плавання, що допомагає зберігати правильне положення тіла у воді. Регульований ремінець і м'який силіконовий наконечник забезпечують комфорт під час тренувань."

    cats.add_product("Swimming", Product(206, "SKU-016", "Плавки чоловічі Joss", 370.00, 30))
    cats._by_id[206].image_url = "/static/swimming/plavky.jpg"
    cats._by_id[206].description = "Чоловічі плавки Joss із швидковисихаючого матеріалу. Ергономічний крій і еластичний пояс забезпечують комфорт і свободу рухів у воді."

    cats.add_product("Swimming", Product(207, "SKU-017", "Купальник жіночий Arena", 780.00, 25))
    cats._by_id[207].image_url = "/static/swimming/kypalnik.webp"
    cats._by_id[207].description = "Жіночий купальник Arena з хлоростійкого матеріалу. Зручний крій і підтримка забезпечують комфорт під час тренувань і змагань."

    cats.add_product("Swimming", Product(208, "SKU-018", "Рушник мікрофібра 70×140", 310.00, 50))
    cats._by_id[208].image_url = "/static/swimming/rushnik.jpg"
    cats._by_id[208].description = "Рушник з мікрофібри розміром 70×140 см. Легкий, швидковисихаючий і компактний — ідеальний для плавання та подорожей."

    # --- HIKING ---
    cats.add_product("Hiking", Product(301, "SKU-021", "Рюкзак трекінговий 45L", 2100.00, 8))
    cats._by_id[301].image_url = "/static/hiking/rykzak.jpg"
    cats._by_id[301].description = "Легкий трекінговий рюкзак об'ємом 45 літрів із регульованою спинкою та поясним ременем. Багато кишень і відділень для зручної організації спорядження."

    cats.add_product("Hiking", Product(302, "SKU-022", "Термос 1L", 480.00, 30))
    cats._by_id[302].image_url = "/static/hiking/termos.jpg"
    cats._by_id[302].description = "Вакуумний термос об'ємом 1 літр із нержавіючої сталі. Зберігає напої гарячими або холодними до 12 годин, має зручну кришку-стакан."

    cats.add_product("Hiking", Product(303, "SKU-023", "Килимок каремат самонадувний", 1200.00, 10))
    cats._by_id[303].image_url = "/static/hiking/karimat.jpg"
    cats._by_id[303].description = "Самонадувний каремат із піни з відкритими порами. Легкий і компактний, забезпечує комфортний сон на природі."

    cats.add_product("Hiking", Product(304, "SKU-024", "Пальник газовий туристичний", 850.00, 15))
    cats._by_id[304].image_url = "/static/hiking/palnyk.webp"
    cats._by_id[304].description = "Компактний газовий пальник для туристів із регульованим вогнем. Легко збирається і підключається до стандартних газових балонів."

    cats.add_product("Hiking", Product(305, "SKU-025", "Ліхтар налобний LED", 640.00, 22))
    cats._by_id[305].image_url = "/static/hiking/lihtar.jpg"
    cats._by_id[305].description = "Налобний ліхтар із світлодіодами високої яскравості. Має кілька режимів роботи, водонепроникний корпус і регульований ремінець для комфортного носіння."

    cats.add_product("Hiking", Product(306, "SKU-026", "Термокружка 0.5L", 320.00, 35))
    cats._by_id[306].image_url = "/static/hiking/kryzhka.jpg"
    cats._by_id[306].description = "Термокружка об'ємом 0.5 літра з подвійними стінками з нержавіючої сталі. Зберігає напої гарячими або холодними до 6 годин, має герметичну кришку."

    cats.add_product("Hiking", Product(307, "SKU-027", "Трекінгові палиці 135см", 980.00, 16))
    cats._by_id[307].image_url = "/static/hiking/palytsi.jpg"
    cats._by_id[307].description = "Легкі алюмінієві трекінгові палиці з регульованою довжиною до 135 см. Ергономічні ручки та амортизуючі наконечники забезпечують комфорт і підтримку на різних типах місцевості."

    cats.add_product("Hiking", Product(308, "SKU-028", "Кросівки трекінгові Salewa", 3450.00, 9))
    cats._by_id[308].image_url = "/static/hiking/krossovki.jpg"
    cats._by_id[308].description = "Трекінгові кросівки Salewa з водонепроникною мембраною і міцною підошвою Vibram. Забезпечують комфорт і підтримку стопи на довгих маршрутах."

    # --- CYCLING (Велоспорт) ---
    cats.add_product("Cycling", Product(401, "SKU-041", "Велосипедний шолом MTB", 1250.00, 18))
    cats._by_id[401].image_url = "/static/cycling/helmet.webp"
    cats._by_id[401].description = "Легкий велосипедний шолом для гірського велосипеда (MTB) з вентиляційними отворами та регульованою системою фіксації. Забезпечує безпеку і комфорт під час їзди по пересіченій місцевості."

    cats.add_product("Cycling", Product(402, "SKU-042", "Рукавички велосипедні", 390.00, 40))
    cats._by_id[402].image_url = "/static/cycling/rykavichki.webp"
    cats._by_id[402].description = "Велосипедні рукавички з амортизуючими вставками на долонях і дихаючою тканиною на тильній стороні. Забезпечують комфорт і захист під час тривалих поїздок."

    cats.add_product("Cycling", Product(403, "SKU-043", "Фара передня 800 лм (USB)", 720.00, 26))
    cats._by_id[403].image_url = "/static/cycling/fara.jpeg"
    cats._by_id[403].description = "Передня фара для велосипеда з яскравістю 800 люменів і зарядкою через USB. Має кілька режимів освітлення і водонепроникний корпус для безпечної їзди в будь-яких умовах."

    cats.add_product("Cycling", Product(404, "SKU-044", "Ліхтар задній строб (USB)", 390.00, 34))
    cats._by_id[404].image_url = "/static/cycling/farazad.jpg"
    cats._by_id[404].description = "Задній ліхтар для велосипеда з режимом стробоскопа і зарядкою через USB. Підвищує видимість і безпеку під час їзди в темний час доби."

    cats.add_product("Cycling", Product(405, "SKU-045", "Насос підлоговий з манометром", 980.00, 15))
    cats._by_id[405].image_url = "/static/cycling/nasos.webp"
    cats._by_id[405].description = "Підлоговий велосипедний насос з манометром для точного вимірювання тиску. Підходить для різних типів клапанів і забезпечує швидке накачування шин."

    cats.add_product("Cycling", Product(406, "SKU-046", "Сідло гелеве Comfort", 860.00, 20))
    cats._by_id[406].image_url = "/static/cycling/sidlo.jpg"
    cats._by_id[406].description = "Гелеве велосипедне сідло Comfort з ергономічним дизайном і додатковою амортизацією. Забезпечує комфорт під час тривалих поїздок і зменшує тиск на сідниці." # type: ignore

    cats.add_product("Cycling", Product(407, "SKU-047", "Ланцюг 11-швидк. KMC", 890.00, 28))
    cats._by_id[407].image_url = "/static/cycling/lancyh.jpg"
    cats._by_id[407].description = "Велосипедний ланцюг KMC для 11-швидкісних трансмісій. Виготовлений з міцної сталі з антикорозійним покриттям для тривалого терміну служби і надійного перемикання передач." 

    cats.add_product("Cycling", Product(408, "SKU-048", "Камера 29\" x 2.10 (AV)", 210.00, 60))
    cats._by_id[408].image_url = "/static/cycling/kamera.jpg"
    cats._by_id[408].description = "Велосипедна камера розміром 29\" x 2.10 з автомобільним клапаном (AV). Виготовлена з якісної гуми для надійного утримання повітря і стійкості до проколів."

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
# print("Total after removal:", cart.calculate_total())
# print("Cart items:", cart.items)
# print("Catalog stock snapshot:", as_dict(catalog))