# app/cart_runtime.py

from __future__ import annotations

from typing import Dict, Iterable, Tuple
from uuid import uuid4
from decimal import Decimal

from sqlalchemy.orm import Session

from .core.database import SessionLocal
from .models import (
    Product,
    Cart,
    CartItem
)


def _price_to_decimal(x) -> Decimal:

    if isinstance(x, Decimal):
        return x

    try:
        return Decimal(str(x))

    except Exception:
        return Decimal("0")


class ShoppingCart:

    def __init__(
        self,
        cid: str
    ):

        self.cid = cid

    # ---------------- INTERNAL ----------------

    def _get_product(
        self,
        db: Session,
        product_id: int
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def _get_cart(
        self,
        db: Session
    ) -> Cart:

        cart = (
            db.query(Cart)
            .filter(
                Cart.session_id == self.cid
            )
            .first()
        )

        if cart is None:

            cart = Cart(
                session_id=self.cid
            )

            db.add(cart)

            db.commit()

            db.refresh(cart)

        return cart

    # ---------------- PUBLIC ----------------

    def add_item(
        self,
        product_id: int,
        qty: int = 1
    ) -> dict:

        if qty <= 0:
            raise ValueError(
                "qty must be positive"
            )

        db: Session = SessionLocal()

        try:

            p = self._get_product(
                db,
                product_id
            )

            if p is None:
                raise KeyError(
                    f"Product {product_id} not found"
                )

            if p.stock < qty:
                raise ValueError(
                    "Not enough stock"
                )

            cart = self._get_cart(db)

            item = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == product_id
                )
                .first()
            )

            p.stock -= qty

            if item:

                item.qty += qty

            else:

                item = CartItem(
                    cart_id=cart.id,
                    product_id=product_id,
                    qty=qty
                )

                db.add(item)

            db.commit()

            return {
                "id": p.id,
                "name": p.name,
                "qty": qty
            }

        finally:

            db.close()

    def remove_item(
        self,
        product_id: int,
        qty: int | None = None
    ) -> int:

        db: Session = SessionLocal()

        try:

            cart = self._get_cart(db)

            item = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == product_id
                )
                .first()
            )

            if item is None:
                return 0

            current = item.qty

            remove_qty = (
                current
                if qty is None
                else min(
                    int(qty),
                    current
                )
            )

            p = self._get_product(
                db,
                product_id
            )

            if p:
                p.stock += remove_qty

            left = current - remove_qty

            if left <= 0:

                db.delete(item)

            else:

                item.qty = left

            db.commit()

            return remove_qty

        finally:

            db.close()

    def clear(self) -> None:

        db: Session = SessionLocal()

        try:

            cart = self._get_cart(db)

            items = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id
                )
                .all()
            )

            for item in items:

                p = self._get_product(
                    db,
                    item.product_id
                )

                if p:
                    p.stock += item.qty

                db.delete(item)

            db.commit()

        finally:

            db.close()

    def count(self) -> int:

        db: Session = SessionLocal()

        try:

            cart = self._get_cart(db)

            items = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id
                )
                .all()
            )

            return sum(
                i.qty
                for i in items
            )

        finally:

            db.close()

    def calculate_total(
        self
    ) -> float:

        db: Session = SessionLocal()

        try:

            cart = self._get_cart(db)

            items = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id
                )
                .all()
            )

            total = Decimal(0)

            for item in items:

                p = self._get_product(
                    db,
                    item.product_id
                )

                if p:

                    total += (
                        _price_to_decimal(
                            p.price
                        )
                        * item.qty
                    )

            return float(total)

        finally:

            db.close()

    def iter_items(
        self
    ) -> Iterable[Tuple[Product, int]]:

        db: Session = SessionLocal()

        try:

            cart = self._get_cart(db)

            items = (
                db.query(CartItem)
                .filter(
                    CartItem.cart_id == cart.id
                )
                .all()
            )

            for item in items:

                p = self._get_product(
                    db,
                    item.product_id
                )

                if p:
                    yield p, item.qty

        finally:

            db.close()


class CartStore:

    def __init__(self):

        self._carts: Dict[
            str,
            ShoppingCart
        ] = {}

    def get_or_create(
        self,
        cid: str
    ) -> ShoppingCart:

        if cid not in self._carts:

            self._carts[cid] = (
                ShoppingCart(cid)
            )

        return self._carts[cid]

    def get(
        self,
        cid: str
    ) -> ShoppingCart:

        return self.get_or_create(cid)


_CART_STORE = CartStore()


def get_or_create_cid(
    request
) -> str:

    cid = request.cookies.get("cid")

    if not cid:
        cid = uuid4().hex

    return cid


def get_cart(
    cid: str
) -> ShoppingCart:

    return _CART_STORE.get(cid)