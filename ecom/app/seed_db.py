from .core.database import SessionLocal
from .models import Category, Product


def seed_database():
    db = SessionLocal()

    # якщо вже є категорії — нічого не робимо
    existing = db.query(Category).first()
    if existing:
        db.close()
        return

    # ---------- categories ----------
    mma = Category(name="MMA")
    swimming = Category(name="Swimming")
    hiking = Category(name="Hiking")
    cycling = Category(name="Cycling")

    db.add_all([mma, swimming, hiking, cycling])
    db.commit()

    # ---------- products ----------
    products = [
        Product(
            id=101,
            sku="SKU-001",
            name="Рукавички MMA",
            description="Легкі рукавички MMA.",
            price=900,
            stock=10,
            image_url="/static/mma/rykavichki.webp",
            category_id=mma.id
        ),

        Product(
            id=102,
            sku="SKU-002",
            name="Капа",
            description="Захист для щелепи.",
            price=180,
            stock=50,
            image_url="/static/mma/kapa.jpg",
            category_id=mma.id
        ),

        Product(
            id=201,
            sku="SKU-003",
            name="Окуляри для плавання Arena",
            description="Окуляри для тренувань.",
            price=350,
            stock=20,
            image_url="/static/swimming/okylary.webp",
            category_id=swimming.id
        ),
    ]

    db.add_all(products)
    db.commit()

    db.close()

    print("DATABASE SEEDED")