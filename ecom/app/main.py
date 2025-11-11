# app/main.py
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote_plus, urlparse, parse_qs, urlencode, urlunparse

# runtime-шари
from .cart_runtime import get_or_create_cid, get_cart, CATALOG

app = FastAPI(title="Ecom MVP")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# ---------- утиліта для безпечного додавання query-параметрів ----------
def _url_with_params(base_url: str, **params) -> str:
    """
    Lодає/оновлює query-параметри у будь-який URL (враховуючи referer з абсолютом/відносним шляхом).
    Якщо щось піде не так — повертає корінь з потрібними параметрами.
    """
    try:
        p = urlparse(base_url)
        q = parse_qs(p.query)
        for k, v in params.items():
            if v is None:
                q.pop(k, None)
            else:
                q[k] = [str(v)]
        new_q = urlencode(q, doseq=True)
        return urlunparse((p.scheme, p.netloc, p.path, p.params, new_q, p.fragment))
    except Exception:
        qs = urlencode({k: v for k, v in params.items() if v is not None})
        return "/" + (f"?{qs}" if qs else "")


# ---------- нормалізатори кошика ----------
def _iter_cart_items(cart):
    """
    Ітератор по позиціях кошика у будь-якому форматі.
      - dict: {pid: qty} або {pid: {"qty": N}}
      - list: [{"product_id"|"pid"|"id": pid, "qty": N}]
    Повертає (pid_int, qty_int)
    """
    items = getattr(cart, "items", None) or {}

    # dict-формат
    if isinstance(items, dict):
        for k, v in items.items():
            try:
                pid = int(k)
            except Exception:
                pid = int(str(k))

            if isinstance(v, dict):
                qty = int(v.get("qty", 0))
            else:
                qty = int(v)

            if qty > 0:
                yield pid, qty
        return

    # list-формат
    if isinstance(items, list):
        for row in items:
            if not isinstance(row, dict):
                continue
            pid_raw = row.get("product_id", row.get("pid", row.get("id")))
            if pid_raw is None:
                continue
            try:
                pid = int(pid_raw)
            except Exception:
                pid = int(str(pid_raw))
            qty = int(row.get("qty", 0))
            if qty > 0:
                yield pid, qty
        return

    # інші варіанти — нічого
    return


def _cart_qty(cart) -> int:
    """Підрахунок кількості товарів у кошику незалежно від структури."""
    try:
        if hasattr(cart, "count") and callable(getattr(cart, "count")):
            return int(cart.count())
    except Exception:
        pass

    total = 0
    try:
        for _, q in _iter_cart_items(cart):
            total += int(q)
    except Exception:
        return 0
    return total


# ---------- шіми для додавання/видалення ----------
def _cart_add(cart, product_id: int, qty: int):
    """
    Додає товар у кошик, навіть якщо немає add_item().
    Спроби:
      1) add_item / add / add_product / add_to_cart
      2) ручне оновлення cart.items (+ зменшення складу, якщо знайдемо товар)
    """
    # офіційні методи, якщо є
    for m in ("add_item", "add", "add_product", "add_to_cart"):
        fn = getattr(cart, m, None)
        if callable(fn):
            return fn(int(product_id), int(qty))

    # ручний режим
    pid = int(product_id)
    q = int(qty)

    # знайти товар і перевірити склад
    p = None
    try:
        p = cart._find_product(pid)
    except Exception:
        p = None

    if p is not None:
        stock_attr = "stock_qty" if hasattr(p, "stock_qty") else ("stock" if hasattr(p, "stock") else None)
        if stock_attr:
            cur = getattr(p, stock_attr, 0) or 0
            if int(cur) < q:
                raise ValueError("Not enough stock")
            try:
                setattr(p, stock_attr, int(cur) - q)
            except Exception:
                pass

    # оновлюємо items
    items = getattr(cart, "items", None)
    if items is None:
        items = {}
        setattr(cart, "items", items)

    if isinstance(items, dict):
        if pid in items:
            if isinstance(items[pid], dict):
                items[pid]["qty"] = int(items[pid].get("qty", 0)) + q
            else:
                items[pid] = int(items[pid]) + q
        else:
            items[pid] = q
        return

    if isinstance(items, list):
        for row in items:
            if not isinstance(row, dict):
                continue
            rid = row.get("product_id", row.get("pid", row.get("id", -1)))
            try:
                rid = int(rid)
            except Exception:
                try:
                    rid = int(str(rid))
                except Exception:
                    rid = -1
            if rid == pid:
                row["qty"] = int(row.get("qty", 0)) + q
                return
        items.append({"product_id": pid, "qty": q})
        return

    # якщо структура невідома — перезапис як dict
    setattr(cart, "items", {pid: q})


def _cart_remove(cart, product_id: int):
    """
    Видаляє позицію з кошика, навіть якщо немає remove_item().
    Повертає кількість, яку прибрали (для повернення на склад за бажанням).
    """
    for m in ("remove_item", "remove", "delete", "remove_from_cart"):
        fn = getattr(cart, m, None)
        if callable(fn):
            return fn(int(product_id))

    pid = int(product_id)
    items = getattr(cart, "items", None)
    removed_qty = 0

    if isinstance(items, dict):
        if pid in items:
            v = items.pop(pid)
            removed_qty = int(v.get("qty", v)) if isinstance(v, dict) else int(v)

    elif isinstance(items, list):
        keep = []
        for row in items:
            if not isinstance(row, dict):
                keep.append(row)
                continue
            rid = row.get("product_id", row.get("pid", row.get("id", -1)))
            try:
                rid = int(rid)
            except Exception:
                try:
                    rid = int(str(rid))
                except Exception:
                    rid = -1
            if rid == pid:
                removed_qty = int(row.get("qty", 0))
            else:
                keep.append(row)
        setattr(cart, "items", keep)

    return removed_qty


# ---------- рендер-хелпер ----------
def _render(request: Request, template: str, ctx: dict):
    cid = get_or_create_cid(request)
    cart = get_cart(cid)

    # ---- визначаємо route для фону
    path = request.url.path
    if path == "/":
        route = "home"
    elif path.startswith("/cart"):
        route = "cart"
    elif path.startswith("/category"):
        route = "category"
    else:
        route = "home"

    qty = _cart_qty(cart)

    ctx.update({
        "request": request,
        "cart_count": qty,
        "cart_qty": qty,
        "route": route,   # для фонів у CSS
    })
    return templates.TemplateResponse(template, ctx)


# ---------- routes ----------
@app.get("/", name="catalog", response_class=HTMLResponse)
async def home(request: Request):
    categories = CATALOG.list_categories()
    preview = {name: CATALOG.get_products(name)[:3] for name in categories}
    resp = _render(request, "index.html", {"categories": categories, "preview": preview})
    if not request.cookies.get("cid"):
        resp.set_cookie("cid", get_or_create_cid(request))
    return resp


@app.get("/category/{name}", name="category", response_class=HTMLResponse)
async def category_page(name: str, request: Request):
    products = CATALOG.get_products(name)
    if not products:
        raise HTTPException(404, detail="category_not_found_or_empty")
    resp = _render(request, "category.html", {"category": name, "products": products})
    if not request.cookies.get("cid"):
        resp.set_cookie("cid", get_or_create_cid(request))
    return resp


@app.get("/cart", name="cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    cid = get_or_create_cid(request)
    cart = get_cart(cid)

    items = []
    for pid, qty in _iter_cart_items(cart):
        # витягуємо продукт
        p = None
        try:
            p = cart._find_product(pid)
        except Exception:
            p = None
        if not p:
            continue

        # ціна -> float
        try:
            price = float(p.price)
        except Exception:
            price = float(str(p.price))

        items.append({
            "product": {
                "id": pid,
                "name": getattr(p, "name", ""),
                "sku": getattr(p, "sku", ""),
                "price": price,
            },
            "qty": int(qty),
            "line_total": round(price * int(qty), 2),
        })

    total = round(sum(i["line_total"] for i in items), 2)

    q = request.query_params
    ctx = {
        "items": items,
        "total": total,
        "subtotal": total,  # сумісність з іншою назвою
        "added": q.get("added"),
        "pid": q.get("pid"),
        "name": q.get("name"),
        "qty": q.get("qty"),
        "error": q.get("error"),
    }
    resp = _render(request, "cart.html", ctx)
    if not request.cookies.get("cid"):
        resp.set_cookie("cid", cid)
    return resp


@app.get("/cart/add", name="cart_add_get")
async def cart_add_get_redirect(request: Request):
    referer = request.headers.get("referer", "/")
    return RedirectResponse(url=referer, status_code=303)


@app.post("/cart/add", name="cart_add")
async def add_to_cart(
    request: Request,
    product_id: int = Form(...),
    qty: int = Form(1),
):
    # нормалізуємо кількість
    try:
        qty = int(qty)
    except Exception:
        qty = 1
    if qty <= 0:
        qty = 1

    cid = get_or_create_cid(request)
    cart = get_cart(cid)
    referer = request.headers.get("referer") or "/"

    try:
        pid = int(product_id)
        _cart_add(cart, pid, qty)  # шім: додає незалежно від API
        if hasattr(cart, "save") and callable(getattr(cart, "save")):
            try:
                cart.save()
            except Exception:
                pass

        p = None
        try:
            p = cart._find_product(pid)
        except Exception:
            p = None
        name = getattr(p, "name", f"#{pid}") if p else f"#{pid}"
        url = _url_with_params(referer,
                               added=1,
                               pid=pid,
                               name=quote_plus(name),
                               qty=qty)
        resp = RedirectResponse(url=url, status_code=303)

    except KeyError:
        url = _url_with_params(referer, error="product_not_found")
        resp = RedirectResponse(url=url, status_code=303)

    except ValueError as e:
        key = "not_enough_stock" if "stock" in str(e).lower() else "bad_qty"
        url = _url_with_params(referer, error=key)
        resp = RedirectResponse(url=url, status_code=303)

    except Exception as e:
        print("ADD_TO_CART_FATAL:", repr(e))
        url = _url_with_params(referer, error="internal")
        resp = RedirectResponse(url=url, status_code=303)

    if not request.cookies.get("cid"):
        resp.set_cookie("cid", cid)
    return resp


@app.post("/cart/remove", name="cart_remove")
async def remove_from_cart(request: Request):
    form = await request.form()
    pid = int(form.get("product_id"))
    next_url = form.get("next_url") or "/cart"

    cid = get_or_create_cid(request)
    cart = get_cart(cid)

    try:
        removed_qty = _cart_remove(cart, pid)
        # повернемо на склад, якщо знайдемо товар і є поле stock/stock_qty
        p = None
        try:
            p = cart._find_product(pid)
        except Exception:
            p = None
        if p is not None and removed_qty > 0:
            stock_attr = "stock_qty" if hasattr(p, "stock_qty") else ("stock" if hasattr(p, "stock") else None)
            if stock_attr:
                try:
                    cur = int(getattr(p, stock_attr, 0) or 0)
                    setattr(p, stock_attr, cur + int(removed_qty))
                except Exception:
                    pass

        if hasattr(cart, "save") and callable(getattr(cart, "save")):
            try:
                cart.save()
            except Exception:
                pass
    except Exception as e:
        print("CART_REMOVE_WARN:", repr(e))

    return RedirectResponse(url=next_url, status_code=303)