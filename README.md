# Shop API

Django REST Framework asosida yozilgan do'kon backend'i: mahsulotlar, buyurtmalar, JWT autentifikatsiya.

## Imkoniyatlar
- JWT bilan login (access/refresh)
- Mahsulotlar: ro'yxat, pagination, filtr
- Buyurtmalar: ichma-ich (nested) items bilan yaratish
- `transaction.atomic` bilan xavfsiz buyurtma yaratish
- Ownership: user faqat o'z buyurtmalarini ko'radi, staff hammasini
- Narx buyurtma paytida OrderItem'ga nusxalanadi
- Validatsiya: bo'sh buyurtma, noto'g'ri miqdor, nofaol mahsulot
- Swagger hujjati, admin panel

## Texnologiyalar
Python, Django, Django REST Framework, PostgreSQL, SimpleJWT, drf-spectacular

## Ishga tushirish
```
git clone https://github.com/shaxbozbek011/mini-shop.git
cd mini-shop
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
`.env` faylida `SECRET_KEY` va baza sozlamalarini to'ldiring.

## API
- Swagger: `/api/docs/`
- `POST /api/token/` : login (access va refresh token)
- `POST /api/token/refresh/` : tokenni yangilash
- `GET, POST /api/products/` : mahsulotlar
- `GET, POST /api/orders/` : buyurtmalar (faqat o'zinikini ko'radi)

## Buyurtma yaratish namunasi
```json
POST /api/orders/
{
  "items": [
    {"product": 1, "quantity": 2}
  ]
}
```

## Muallif
Shaxboz, Telegram: @https://t.me/bakirovich_sh