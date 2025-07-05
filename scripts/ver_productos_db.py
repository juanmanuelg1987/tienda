from flask import Flask
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
    print(f"Total productos en DB: {len(productos)}\n")
    for p in productos[:20]:
        print(f"ID: {p.id} | Nombre: {p.name} | Precio: {p.price}")
    if len(productos) > 20:
        print("... (solo se muestran los primeros 20)")
