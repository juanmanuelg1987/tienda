# models.py
# Definición de los modelos de datos para el portal de ventas online
# Incluye: Usuario, Producto y Pedido

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    # Modelo de producto para el catálogo
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=True)  # URL o ruta de imagen
    category = db.Column(db.String(20), nullable=False, default='perro')  # 'perro' o 'gato'

#class Order(db.Model):
#    # Modelo de pedido (muy simple)
#    id = db.Column(db.Integer, primary_key=True)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#    # Aquí podrías agregar más campos como fecha, estado, etc.
