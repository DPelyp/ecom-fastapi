# app/main.py
from pathlib import Path
from urllib.parse import (
    quote_plus,
    urlparse,
    parse_qs,
    urlencode,
    urlunparse
)

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Form,
    Depends
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .core.database import (
    engine,
    Base,
    get_db
)

from .models import (
    Category,
    Product
)

from .seed_db import seed_database

from .cart_runtime import (
    get_or_create_cid,
    get_cart
)

app = FastAPI(title="Ecom MVP")

# ---------------- DB ----------------

Base.metadata.create_all(bind=engine)

seed_database()

# ---------------- PATHS ----------------

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

# ---------------- HELPERS ----------------

def _url_with_params(base_url: str, **params) -> str:
    try:
        p = urlparse(base_url)

        q = parse_qs(p.query)

        for k, v in params.items():
            if v is None:
                q.pop(k, None)
            else:
                q[k] = [str(v)]

        new_q = urlencode(q, doseq=True)

        return urlunparse(
            (
                p.scheme,
                p.netloc,
                p.path,
                p.params,
                new_q,
                p.fragment
            )
        )

    except Exception:
        qs = urlencode(
            {
                k: v
                for k, v in params.items()
                if v is not None
            }
        )

        return "/" + (f"?{qs}" if qs else "")

def _cart_add(cart, product_id: int, qty: int):

    pid = int(product_id)
    q = int(qty)

    items = getattr(cart, "items", None)

    if items is None:
        items = {}
        setattr(cart, "items", items)

    if pid in items:
        items[pid] += q
    else:
        items[pid] = q
def _render(
    request: Request,
    template: str,
    ctx: dict
):

    cid = get_or_create_cid(request)

    cart = get_cart(cid)

    path = request.url.path

    if path == "/":
        route = "home"

    elif path.startswith("/cart"):
        route = "cart"

    elif path.startswith("/category"):
        route = "category"

    else:
        route = "home"

    qty = cart.count()

    ctx.update(
        {
            "request": request,
            "cart_count": qty,
            "cart_qty": qty,
            "route": route
        }
    )

    return templates.TemplateResponse(
        template,
        ctx
    )
# ---------------- ROUTES ----------------

@app.get(
    "/",
    name="catalog",
    response_class=HTMLResponse
)
async def home(
    request: Request,
    db: Session = Depends(get_db)
):

    categories = db.query(Category).all()

    preview = {}

    for category in categories:
        preview[category.name] = category.products[:3]

    resp = _render(
        request,
        "index.html",
        {
            "categories": categories,
            "preview": preview
        }
    )

    if not request.cookies.get("cid"):
        resp.set_cookie(
            "cid",
            get_or_create_cid(request)
        )

    return resp


@app.get(
    "/category/{name}",
    name="category",
    response_class=HTMLResponse
)
async def category_page(
    name: str,
    request: Request,
    db: Session = Depends(get_db)
):

    category = db.query(Category).filter(
        Category.name == name
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="category_not_found"
        )

    products = category.products

    resp = _render(
        request,
        "category.html",
        {
            "category": category,
            "products": products
        }
    )

    if not request.cookies.get("cid"):
        resp.set_cookie(
            "cid",
            get_or_create_cid(request)
        )

    return resp

@app.get(
    "/cart",
    name="cart",
    response_class=HTMLResponse
)
async def view_cart(
    request: Request,
    db: Session = Depends(get_db)
):

    cid = get_or_create_cid(request)

    cart = get_cart(cid)

    items = []

    for p, qty in cart.iter_items():

        price = float(p.price)

        items.append(
            {
                "product": {
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "price": price,
                },

                "qty": int(qty),

                "line_total": round(
                    price * int(qty),
                    2
                ),
            }
        )

    total = round(
        sum(
            i["line_total"]
            for i in items
        ),
        2
    )

    resp = _render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
            "subtotal": total,
        }
    )

    if not request.cookies.get("cid"):

        resp.set_cookie(
            "cid",
            cid
        )

    return resp


@app.post(
    "/cart/add",
    name="cart_add"
)
async def add_to_cart(
    request: Request,
    product_id: int = Form(...),
    qty: int = Form(1),
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="product_not_found"
        )

    if product.stock < qty:
        raise HTTPException(
            status_code=400,
            detail="not_enough_stock"
        )

    cid = get_or_create_cid(request)

    cart = get_cart(cid)

    cart.add_item(
        product_id,
        qty
    )

    referer = request.headers.get(
        "referer",
        "/"
    )

    url = _url_with_params(
        referer,
        added=1,
        pid=product.id,
        name=quote_plus(product.name),
        qty=qty
    )

    resp = RedirectResponse(
        url=url,
        status_code=303
    )

    if not request.cookies.get("cid"):
        resp.set_cookie("cid", cid)

    return resp
@app.post(
    "/cart/remove",
    name="cart_remove"
)
async def remove_from_cart(
    request: Request
):

    form = await request.form()

    pid = int(
        form.get("product_id")
    )

    next_url = form.get(
        "next_url",
        "/cart"
    )

    cid = get_or_create_cid(request)

    cart = get_cart(cid)

    cart.remove_item(pid)

    return RedirectResponse(
        url=next_url,
        status_code=303
    )

@app.get(
    "/product/{product_id}",
    response_class=HTMLResponse
)
async def product_page(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Товар не знайдено"
        )

    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product
        }
    )