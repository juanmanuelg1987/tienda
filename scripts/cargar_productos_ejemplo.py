# Script para cargar 6 productos completos de ejemplo en la base de datos Flask
# Ejecuta este script una sola vez con: python scripts/cargar_productos_ejemplo.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from models import Product

productos = [
    {
        'name': 'Purina Excellent Adulto Pollo y Arroz',
        'description': 'Alimento balanceado premium para perros adultos de razas medianas y grandes. Con proteínas de alta calidad y arroz para una digestión saludable.',
        'price': 28999.00,
        'stock': 20,
        'image_url': 'img/excellent-adulto-pollo-arroz.jpg',
        'category': 'perro',
    },
    {
        'name': 'Pro Plan Perro Adulto Razas Medianas',
        'description': 'Nutrición avanzada con OptiLife para perros adultos de raza mediana. Refuerza defensas y vitalidad.',
        'price': 32999.00,
        'stock': 15,
        'image_url': 'img/proplan-adulto-mediano.jpg',
        'category': 'perro',
    },
    {
        'name': 'Royal Canin Mini Adult',
        'description': 'Alimento para perros adultos de raza pequeña. Fórmula exclusiva para energía, vitalidad y pelaje sano.',
        'price': 31500.00,
        'stock': 12,
        'image_url': 'img/royalcanin-mini.jpg',
        'category': 'perro',
    },
    {
        'name': 'Purina Excellent Gato Adulto Pollo y Arroz',
        'description': 'Alimento completo para gatos adultos. Con pollo, arroz y fibras para una digestión óptima y pelaje brillante.',
        'price': 21999.00,
        'stock': 18,
        'image_url': 'img/excellent-gato-adulto.jpg',
        'category': 'gato',
    },
    {
        'name': 'Pro Plan Gato Adulto',
        'description': 'Nutrición avanzada para gatos adultos. Ayuda a mantener un pelaje brillante y un sistema inmunológico fuerte.',
        'price': 24999.00,
        'stock': 10,
        'image_url': 'img/proplan-gato-adulto.jpg',
        'category': 'gato',
    },
    {
        'name': 'Royal Canin Gato Sterilised',
        'description': 'Alimento para gatos adultos esterilizados. Controla el peso y cuida el tracto urinario.',
        'price': 23700.00,
        'stock': 14,
        'image_url': 'img/royalcanin-gato-sterilised.jpg',
        'category': 'gato',
    },
]

with app.app_context():
    for prod in productos:
        existe = Product.query.filter_by(name=prod['name']).first()
        if not existe:
            p = Product(**prod)
            db.session.add(p)
    db.session.commit()
    print('Productos de ejemplo cargados exitosamente.')
