# 🏋️‍♂️ Ecom FastAPI — спортивний онлайн-магазин

Невеликий демонстраційний e-commerce проєкт на **FastAPI**, який показує:
- динамічний каталог товарів
- кошик із додаванням і видаленням позицій
- систему категорій (MMA, Hiking, Swimming)
- адаптивний дизайн із темною/світлою темами

---

## 🚀 Технології
- **Python 3.12**
- **FastAPI** + Jinja2 Templates
- **HTML / CSS (custom dark theme)**
- **SQLite** для бази
- **Uvicorn** як сервер

---

## ⚙️ Запуск локально
```bash
git clone https://github.com/DmytroPelyp/ecom-fastapi.git
cd ecom
pip install -r requirements.txt
uvicorn app.main:app --reload
