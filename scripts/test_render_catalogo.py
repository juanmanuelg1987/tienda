from flask import Flask, render_template_string
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Product, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    productos = Product.query.order_by(Product.id).all()
    # Cargar el template index.html
    with open(os.path.join(os.path.dirname(__file__), '../templates/index.html'), encoding='utf-8') as f:
        tpl = f.read()
    # Renderizar el template con todos los productos
    html = render_template_string(tpl, products=productos, featured_products=productos[:6])
    # Contar cuántas tarjetas de producto aparecen
    cards = html.count('class="col producto-card"')
    print(f"Productos en DB: {len(productos)}")
    print(f"Tarjetas de producto renderizadas: {cards}")
    if cards < len(productos):
        print("ADVERTENCIA: No se están mostrando todos los productos en el catálogo web.")
    else:
        print("OK: Se muestran todos los productos en el catálogo web.")
