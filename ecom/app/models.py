from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)
    description = Column(String)

    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    image_url = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")