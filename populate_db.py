import os
from app import db, Product

def populate():
    if Product.query.first():
        print("La base de datos ya tiene productos. No se agrega nada.")
        return
    productos = [
        {
            "name": "Pro Plan Adulto",
            "price": 25000.0,
            "stock": 10,
            "category": "perro",
            "image_url": "img/productos/proplanadulto.jpeg"
        },
        {
            "name": "Cat Chow Gatitos",
            "price": 18000.0,
            "stock": 15,
            "category": "gato",
            "image_url": "img/productos/catchowgatitos.jpeg"
        },
        {
            "name": "Dog Chow Adulto",
            "price": 22000.0,
            "stock": 8,
            "category": "perro",
            "image_url": "img/productos/dogchowadulto.jpeg"
        }
    ]
    for p in productos:
        prod = Product(**p)
        db.session.add(prod)
    db.session.commit()
    print(f"Se agregaron {len(productos)} productos de ejemplo.")

if __name__ == "__main__":
    populate()
