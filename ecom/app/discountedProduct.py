from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from .core.database import Base


class Category(Base):

    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    products = relationship(
        "Product",
        back_populates="category"
    )


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sku = Column(
        String,
        unique=True,
        nullable=False
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(String)

    price = Column(
        Float,
        nullable=False
    )

    stock = Column(
        Integer,
        default=0
    )

    image_url = Column(String)

    discount_percent = Column(
        Integer,
        default=0
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    # ----------------------------------------
    # BUSINESS LOGIC
    # ----------------------------------------

    @property
    def has_discount(self) -> bool:

        return self.discount_percent > 0

    def final_price(self) -> float:

        price = Decimal(str(self.price))

        discount = (
            Decimal(str(self.discount_percent))
            / Decimal("100")
        )

        result = (
            price
            * (Decimal("1") - discount)
        )

        return float(round(result, 2))

def can_reserve(
    self,
    qty: int
) -> bool:

    qty = int(qty)

    stock = int(self.stock or 0)

    return (
        qty > 0
        and stock >= qty
    )

    def reserve(
        self,
        qty: int
    ):

        qty = int(qty)

        if not self.can_reserve(qty):

            raise ValueError(
                "Not enough stock"
            )

        self.stock -= qty

    def release(
        self,
        qty: int
    ):

        qty = int(qty)

        self.stock += qty

    def __repr__(self):

        return (
            f"Product("
            f"id={self.id}, "
            f"sku='{self.sku}', "
            f"name='{self.name}', "
            f"price={self.price}, "
            f"stock={self.stock}, "
            f"discount={self.discount_percent}%"
            f")"
        )