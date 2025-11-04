# app/goodsCategories.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

from typing import List, Dict
from .goodsProducts import Product

class GoodsCategories:
    def __init__(self):
        # назва категорії -> список Product
        self.categories: Dict[str, List[Product]] = {}
        # простий індекс всіх товарів за id (знадобиться для пошуку)
        self._by_id: Dict[int, Product] = {}

    def add_category(self, name: str):
        if name not in self.categories:
            self.categories[name] = []

    def add_product(self, category_name: str, product: Product):
        if category_name not in self.categories:
            raise ValueError("category_not_found")
        if product.id in self._by_id:
            raise ValueError("product_id_exists")
        self.categories[category_name].append(product)
        self._by_id[product.id] = product

    def get_products(self, category_name: str):
        return list(self.categories.get(category_name, []))

    def list_categories(self):
        return list(self.categories.keys())

    def get_product_by_id(self, pid: int) -> Product | None:
        return self._by_id.get(pid)
    
    def __repr__(self):
        # коротка форма для дебагу
        return f"<GoodsCategories categories={list(self.categories.keys())}>"

    def __str__(self):
        # більш детальний, людиночитний формат
        lines = []
        for cat, products in self.categories.items():
            # lines.append(f"\nКатегорія: {cat}")
            for p in products:
                lines.append(f"Назва : {p.name} Ціна : {p.price} грн, Кількість : {p.stock_qty} шт.")
        return "\n".join(lines)
