# scripts/importar_articulos.py
"""
Importa los artículos desde articulos_limpios.csv a la base de datos SQLite (app.db)
Mapea:
- nombre -> name
- col1 -> price (si es numérico, sino 0)
- description, stock, image_url quedan vacíos o por defecto
- category queda 'perro' por defecto
"""
import pandas as pd
import sys
import os
from flask import Flask
# Agregar la carpeta raíz al path para importar models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Product, db

# Inicializar Flask y SQLAlchemy igual que en init_db.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Leer el CSV
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articulos_limpios.csv')
df = pd.read_csv(csv_path)

import re

def parse_price(val):
    try:
        # Quitar comas, puntos, espacios, etc. y convertir a float
        val = str(val).replace(",", "").replace("$", "").strip()
        return float(val)
    except:
        return 0.0

count = 0
with app.app_context():
    for _, row in df.iterrows():
        name = str(row.get('nombre', '')).strip()
        if not name or name.lower() == 'nan' or name.lower().startswith('linea'):
            continue  # Omitir filas vacías, 'nan' o encabezados
        price = parse_price(row.get('col1', 0))
        if price != price:  # NaN check
            price = 0.0
        producto = Product(
            name=name,
            price=price,
            description=None,
            stock=0,
            image_url=None,
            category='perro'  # O 'gato' si lo querés ajustar
        )
        db.session.add(producto)
        count += 1
    db.session.commit()
print(f"Se importaron {count} productos a la base de datos app.db.")
