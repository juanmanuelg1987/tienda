import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db
from app import app
from models import Product

CSV_PATH = os.path.join(os.path.dirname(__file__), 'ejemplo_productos_puppis.csv')

with app.app_context():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Evita duplicados por nombre
            if Product.query.filter_by(name=row['name']).first():
                print(f"Ya existe: {row['name']}")
                continue
            product = Product(
                name=row['name'],
                description=row['description'],
                price=float(row['price']) if row['price'] else 0.0,
                stock=10,  # Stock por defecto, puedes ajustar
                image_url=row['image_url'],
                category=row['category'] or 'perro'
            )
            db.session.add(product)
            print(f"Agregado: {product.name}")
    db.session.commit()
    print("Importación finalizada.")
