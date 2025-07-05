import csv
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
    with open('productos_db.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'price', 'stock', 'category'])
        for p in productos:
            writer.writerow([p.id, p.name, p.price, p.stock, p.category])
    print(f"Exportados {len(productos)} productos a productos_db.csv")
