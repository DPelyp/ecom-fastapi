from .goodsProducts import Product
from decimal import Decimal

class DiscountedProduct(Product):
    def __init__(self, *args, discount=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.discount = Decimal(discount)

    def final_price(self):
        return self.price * (Decimal("1") - self.discount)

    def __repr__(self):
        return (
            f"DiscountedProduct(id={self.id}, sku='{self.sku}', "
            f"name='{self.name}', price={self.price} грн, "
            f"discount={self.discount}, stock={self.stock_qty})"
        )
    
    @property
    def has_discount(self) -> bool:
        return self.discount > 0

    @property
    def discount_percent(self) -> int:
        return int(self.discount * 100)