# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .catalog_seed import seed_catalog
from decimal import Decimal
from uuid import uuid4

app = FastAPI(title="Ecom MVP")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
CATALOG = seed_catalog()

# ---- In-memory cart (cookie 'cid')
class CartItem:
    def __init__(self, product_id: int, name: str, price: Decimal, qty: int = 1):
        self.product_id = product_id
        self.name = name
        self.price = Decimal(str(price))
        self.qty = int(qty)
    @property
    def line_total(self) -> Decimal:
        return self.price * self.qty

class Cart:
    def __init__(self):
        self.items: dict[int, CartItem] = {}
    def add(self, product_id: int, name: str, price: Decimal, qty: int = 1):
        if product_id in self.items:
            self.items[product_id].qty += qty
        else:
            self.items[product_id] = CartItem(product_id, name, price, qty)
    def remove(self, product_id: int):
        self.items.pop(product_id, None)
    def count(self) -> int:
        return sum(i.qty for i in self.items.values())
    def subtotal(self) -> Decimal:
        return sum((i.line_total for i in self.items.values()), Decimal("0"))

CARTS: dict[str, Cart] = {}

def _get_or_create_cid(request: Request) -> str:
    cid = request.cookies.get("cid")
    if not cid:
        cid = uuid4().hex
    if cid not in CARTS:
        CARTS[cid] = Cart()
    return cid

def _render(request: Request, template: str, ctx: dict):
    cid = _get_or_create_cid(request)
    cart = CARTS[cid]
    ctx.update({"request": request, "cart_count": cart.count()})
    return templates.TemplateResponse(template, ctx)

# ---- Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    categories = CATALOG.list_categories()
    preview = {name: CATALOG.get_products(name)[:3] for name in categories}
    resp = _render(request, "index.html", {"categories": categories, "preview": preview})
    if not request.cookies.get("cid"):
        resp.set_cookie("cid", _get_or_create_cid(request))
    return resp

@app.get("/category/{name}", response_class=HTMLResponse)
async def category_page(name: str, request: Request):
    products = CATALOG.get_products(name)
    if not products:
        raise HTTPException(404, detail="category_not_found_or_empty")
    return _render(request, "category.html", {"category": name, "products": products})

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    cid = _get_or_create_cid(request)
    cart = CARTS[cid]
    return _render(request, "cart.html", {"items": list(cart.items.values()), "subtotal": cart.subtotal()})

@app.post("/cart/add")
async def add_to_cart(request: Request):
    form = await request.form()
    pid = int(form.get("product_id"))
    qty = int(form.get("qty", 1))
    product = CATALOG.get_product_by_id(pid)
    if not product:
        raise HTTPException(404, detail="product_not_found")
    cid = _get_or_create_cid(request)
    CARTS[cid].add(product.id, product.name, product.price, qty)
    return RedirectResponse(url="/cart", status_code=303)

@app.post("/cart/remove")
async def remove_from_cart(request: Request):
    form = await request.form()
    pid = int(form.get("product_id"))
    cid = _get_or_create_cid(request)
    CARTS[cid].remove(pid)
    return RedirectResponse(url="/cart", status_code=303)