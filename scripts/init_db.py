# scripts/init_db.py
"""
Este script inicializa la base de datos SQLite (app.db) y crea las tablas definidas en models.py.
Solo necesitás ejecutarlo una vez (o cada vez que cambies la estructura de los modelos).
"""
from flask import Flask
import sys
import os
# Agregar la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db

app = Flask(__name__)
# Configuración para usar SQLite en la raíz del proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Base de datos y tablas creadas correctamente (app.db)")
