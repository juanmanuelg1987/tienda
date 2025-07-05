import csv
import re
from flask import Flask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Product, db

def parse_precio(precio_str):
    if not precio_str:
        return None
    precio_str = precio_str.replace('$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(precio_str)
    except Exception:
        return None

PDF_CSV = 'precios_extraidos_pdf.csv'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cargar pares (nombre, precio) del CSV extraído del PDF
def cargar_precios():
    pares = []
    with open(PDF_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Cada fila puede tener hasta dos productos
            if len(row) >= 2 and row[0] and row[1]:
                nombre1 = row[0].strip()
                precio1 = parse_precio(row[1])
                if nombre1 and precio1:
                    pares.append((nombre1, precio1))
            if len(row) >= 5 and row[3] and row[4]:
                nombre2 = row[3].strip()
                precio2 = parse_precio(row[4])
                if nombre2 and precio2:
                    pares.append((nombre2, precio2))
    return pares

with app.app_context():
    precios_pdf = cargar_precios()
    actualizados = 0
    no_encontrados = []
    import re
    def normalizar(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    productos_db = Product.query.all()
    nombres_db = {normalizar(p.name): p for p in productos_db}
    actualizados = 0
    no_encontrados = []
    for nombre_pdf, precio_pdf in precios_pdf:
        key_pdf = normalizar(nombre_pdf)
        prod = nombres_db.get(key_pdf)
        if prod:
            prod.price = precio_pdf
            actualizados += 1
            continue
        # Match parcial si no hay exacto
        match = None
        for k, p in nombres_db.items():
            if key_pdf in k or k in key_pdf:
                match = p
                break
        if match:
            match.price = precio_pdf
            actualizados += 1
        else:
            no_encontrados.append(nombre_pdf)
    db.session.commit()
    print(f"Precios actualizados para {actualizados} productos.")
    if no_encontrados:
        print(f"No se encontraron coincidencias para {len(no_encontrados)} productos del PDF. Ejemplos:")
        for n in no_encontrados[:10]:
            print(f" - {n}")
