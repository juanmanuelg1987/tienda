import sys
import os
import pdfplumber
import csv
import re
from flask import Flask
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Product, db

# Configuración
PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\juan_\Downloads\LISTA DE PRECIOS  CH 27.06.2025.pdf"
CSV_TEMP = "precios_temp.csv"
REPORTE_NO_ENCONTRADOS = "reporte_no_encontrados.csv"

# Paso 1: Extraer productos y precios del PDF a un CSV temporal
def extraer_tabla_pdf(pdf_path, csv_out):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and any(cell and cell.strip() for cell in row):
                        rows.append([cell.strip() if cell else '' for cell in row])
    with open(csv_out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
    return rows

def parse_precio(precio_str):
    if not precio_str:
        return None
    precio_str = precio_str.replace('$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(precio_str)
    except Exception:
        return None

# Paso 2: Leer pares (nombre, precio) del CSV temporal
def cargar_precios(csv_path):
    pares = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
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

# Paso 3: Actualizar precios en la base de datos con match flexible
def actualizar_precios(pares):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        def normalizar(s):
            return re.sub(r"[^a-z0-9]", "", s.lower())
        productos_db = Product.query.all()
        nombres_db = {normalizar(p.name): p for p in productos_db}
        actualizados = 0
        no_encontrados = []
        for nombre_pdf, precio_pdf in pares:
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
                no_encontrados.append((nombre_pdf, precio_pdf))
        db.session.commit()
        return actualizados, no_encontrados

if __name__ == "__main__":
    print(f"Extrayendo productos y precios de: {PDF_PATH}")
    extraer_tabla_pdf(PDF_PATH, CSV_TEMP)
    pares = cargar_precios(CSV_TEMP)
    print(f"Total productos extraídos del PDF: {len(pares)}")
    actualizados, no_encontrados = actualizar_precios(pares)
    print(f"Precios actualizados para {actualizados} productos en la base de datos.")
    print(f"No se encontraron coincidencias para {len(no_encontrados)} productos del PDF.")
    # Guardar reporte de no encontrados
    with open(REPORTE_NO_ENCONTRADOS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['nombre_pdf', 'precio_pdf'])
        for nombre, precio in no_encontrados:
            writer.writerow([nombre, precio])
    print(f"Reporte de productos no encontrados guardado en {REPORTE_NO_ENCONTRADOS}")
