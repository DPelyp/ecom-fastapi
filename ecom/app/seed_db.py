from sqlalchemy.orm import Session

from .core.database import SessionLocal
from .models import Category, Product


def seed_database():

    db: Session = SessionLocal()

    try:

        # ----------------------------------------
        # PROTECTION AGAINST DUPLICATE SEED
        # ----------------------------------------

        if db.query(Category).first():
            return

        # ----------------------------------------
        # CATEGORIES
        # ----------------------------------------

        mma = Category(name="MMA")
        swimming = Category(name="Swimming")
        hiking = Category(name="Hiking")
        cycling = Category(name="Cycling")

        db.add_all([
            mma,
            swimming,
            hiking,
            cycling
        ])

        db.commit()

        # ----------------------------------------
        # PRODUCTS
        # ----------------------------------------

        products = [

            # ================= MMA =================

            Product(
                id=101,
                sku="SKU-001",
                name="Рукавички MMA",

                description=(
                    "Легкі рукавички MMA з щільною амортизацією "
                    "та м’якою підкладкою. Вентиляційні отвори й "
                    "надійна липучка для фіксації."
                ),

                price=900.00,
                stock=10,

                image_url="/static/mma/gloves.avif",

                discount_percent=15,

                category_id=mma.id
            ),

            Product(
                id=102,
                sku="SKU-002",
                name="Капа",

                description=(
                    "Двошарова термопластична капа, "
                    "що формується у гарячій воді."
                ),

                price=180.00,
                stock=50,

                image_url="/static/mma/kapa.jpg",

                category_id=mma.id
            ),

            Product(
                id=103,
                sku="SKU-003",
                name="Шолом боксерський Everlast",

                description=(
                    "Шолом Everlast із багатошаровою "
                    "піною та розширеним кутом огляду."
                ),

                price=1250.00,
                stock=7,

                image_url="/static/mma/helmet.webp",

                category_id=mma.id
            ),

            Product(
                id=104,
                sku="SKU-004",
                name="Бинти еластичні RDX 4.5м",

                description=(
                    "Еластичні бинти RDX "
                    "для стабілізації зап’ястя."
                ),

                price=250.00,
                stock=40,

                image_url="/static/mma/binty.jpg",

                category_id=mma.id
            ),

            Product(
                id=105,
                sku="SKU-005",
                name="Мішок боксерський 30 кг",

                description=(
                    "Боксерський мішок "
                    "із міцної екошкіри."
                ),

                price=2300.00,
                stock=4,

                image_url="/static/mma/grusha.webp",

                category_id=mma.id
            ),

            Product(
                id=106,
                sku="SKU-006",
                name="Лапи тренувальні",

                description=(
                    "Пара тренувальних лап "
                    "для відпрацювання серій."
                ),

                price=720.00,
                stock=12,

                image_url="/static/mma/lapy.jpg",

                category_id=mma.id
            ),

            Product(
                id=107,
                sku="SKU-007",
                name="Кимоно для BJJ",

                description=(
                    "Кімоно для BJJ "
                    "зі щільної плетінки."
                ),

                price=1800.00,
                stock=6,

                image_url="/static/mma/kimono.jpg",

                category_id=mma.id
            ),

            Product(
                id=108,
                sku="SKU-008",
                name="Тайський пад",

                description=(
                    "Щит для ударів "
                    "із щільною піною."
                ),

                price=950.00,
                stock=9,

                image_url="/static/mma/shield.jpg",

                category_id=mma.id
            ),

            # ================= SWIMMING =================

            Product(
                id=201,
                sku="SKU-011",
                name="Окуляри Arena",

                description=(
                    "Окуляри для плавання "
                    "з антифогом."
                ),

                price=350.00,
                stock=25,

                image_url="/static/swimming/glasses.webp",

                category_id=swimming.id
            ),

            Product(
                id=202,
                sku="SKU-012",
                name="Шапочка Speedo",

                description=(
                    "Силіконова шапочка "
                    "для плавання."
                ),

                price=280.00,
                stock=30,

                image_url="/static/swimming/shapochka.webp",

                category_id=swimming.id
            ),

            Product(
                id=203,
                sku="SKU-013",
                name="Ласти тренувальні",

                description=(
                    "Короткі ласти "
                    "для тренувань."
                ),

                price=950.00,
                stock=15,

                image_url="/static/swimming/lasty.jpg",

                category_id=swimming.id
            ),

            Product(
                id=204,
                sku="SKU-014",
                name="Дошка EVA",

                description=(
                    "Дошка для плавання "
                    "з EVA-піни."
                ),

                price=520.00,
                stock=20,

                image_url="/static/swimming/doshka.jpg",

                category_id=swimming.id
            ),

            # ================= HIKING =================

            Product(
                id=301,
                sku="SKU-021",
                name="Рюкзак трекінговий 45L",

                description=(
                    "Трекінговий рюкзак "
                    "об'ємом 45 літрів."
                ),

                price=2100.00,
                stock=8,

                image_url="/static/hiking/rykzak.jpg",

                category_id=hiking.id
            ),

            Product(
                id=302,
                sku="SKU-022",
                name="Термос 1L",

                description=(
                    "Вакуумний термос "
                    "з нержавіючої сталі."
                ),

                price=480.00,
                stock=30,

                image_url="/static/hiking/termos.jpg",

                category_id=hiking.id
            ),

            Product(
                id=303,
                sku="SKU-023",
                name="Каремат самонадувний",

                description=(
                    "Самонадувний "
                    "туристичний каремат."
                ),

                price=1200.00,
                stock=10,

                image_url="/static/hiking/karimat.jpg",

                category_id=hiking.id
            ),

            Product(
                id=304,
                sku="SKU-024",
                name="Газовий пальник",

                description=(
                    "Компактний "
                    "туристичний пальник."
                ),

                price=850.00,
                stock=15,

                image_url="/static/hiking/palnyk.webp",

                category_id=hiking.id
            ),

            # ================= CYCLING =================

            Product(
                id=401,
                sku="SKU-041",
                name="Велошолом MTB",

                description=(
                    "Легкий MTB-шолом "
                    "із вентиляцією."
                ),

                price=1250.00,
                stock=18,

                image_url="/static/cycling/helmet.webp",

                category_id=cycling.id
            ),

            Product(
                id=402,
                sku="SKU-042",
                name="Велорукавички",

                description=(
                    "Велосипедні рукавички "
                    "з амортизацією."
                ),

                price=390.00,
                stock=40,

                image_url="/static/cycling/rykavichki.webp",

                category_id=cycling.id
            ),

            Product(
                id=403,
                sku="SKU-043",
                name="Фара 800 лм",

                description=(
                    "Передня велосипедна "
                    "USB-фара."
                ),

                price=720.00,
                stock=26,

                image_url="/static/cycling/fara.jpeg",

                category_id=cycling.id
            ),

            Product(
                id=404,
                sku="SKU-044",
                name="Ліхтар задній",

                description=(
                    "Задній USB-ліхтар "
                    "зі стробоскопом."
                ),

                price=390.00,
                stock=34,

                image_url="/static/cycling/farazad.jpg",

                category_id=cycling.id
            ),
        ]

        db.add_all(products)

        db.commit()

    finally:

        db.close()