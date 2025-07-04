import csv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db, app
from models import Product

CSV_PATH = r'C:\Users\juan_\Downloads\lista - Table 3.csv'

with app.app_context():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue
            name = row[0].strip()
            # Buscar precio en la segunda o tercera columna, quitando símbolos y separadores
            price = None
            for cell in row[1:4]:
                cell = cell.strip().replace('$','').replace('.','').replace(',','.')
                try:
                    price = float(cell)
                    break
                except Exception:
                    continue
            if price is None:
                continue
            # Evita duplicados por nombre
            if Product.query.filter_by(name=name).first():
                print(f"Ya existe: {name}")
                continue
            product = Product(
                name=name,
                price=price,
                stock=10,  # Stock por defecto
                category='perro',
                description='',
                image_url=None
            )
            db.session.add(product)
            print(f"Agregado: {product.name} - ${product.price}")
    db.session.commit()
    print("Importación finalizada.")
