# app.py
# Punto de entrada de la aplicación Flask para el portal de ventas online
# Aquí se configuran las rutas principales y la inicialización de la app

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
# Eliminado Flask-Login para login
from models import db, User, Product, Order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cambia_esto_por_una_clave_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)





@app.route('/')
def index():
    # Página principal: muestra el catálogo de productos
    products = Product.query.all()
    # Selecciona los primeros 3 productos como destacados (puedes cambiar la lógica)
    featured_products = Product.query.limit(3).all()
    return render_template('index.html', products=products, featured_products=featured_products)

    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registro de usuario nuevo
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'warning')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/cart')

def cart():
    # Página del carrito de compras (simple, por sesión)
    cart = session.get('cart', {})
    products = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            products.append({'product': product, 'qty': qty})
            total += product.price * qty
    return render_template('cart.html', products=products, total=total)

@app.route('/add_to_cart/<int:product_id>')

def add_to_cart(product_id):
    # Agrega un producto al carrito
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('index'))

@app.route('/checkout')

def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('El carrito está vacío', 'warning')
        return redirect(url_for('cart'))
    # Construir resumen para la plantilla
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'name': product.name,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render_template('checkout.html', cart_items=cart_items, total=total)


# Puedes agregar aquí más rutas para administración, gestión de productos, etc.

if __name__ == '__main__':
    # Crea las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()
        # Insertar productos de ejemplo si la base está vacía
        if Product.query.count() == 0:
            productos = [
                Product(
                    name='ProPlan Adulto',
                    description='Alimento balanceado para perros adultos. Bolsa 15kg.',
                    price=32000,
                    stock=10,
                    image_url='img/proplan.jpg',
                    category='perro'
                ),
                Product(
                    name='Royal Canin Gato',
                    description='Alimento premium para gatos adultos. Bolsa 7.5kg.',
                    price=28000,
                    stock=8,
                    image_url='img/royalcanin.jpg',
                    category='gato'
                ),
                Product(
                    name='Dog Chow Cachorros',
                    description='Alimento para cachorros, 8kg.',
                    price=18000,
                    stock=15,
                    image_url='img/dogchow.jpg',
                    category='perro'
                ),
                Product(
                    name='Whiskas Adulto',
                    description='Alimento seco para gatos adultos, 10kg.',
                    price=21000,
                    stock=12,
                    image_url='img/whiskas.jpg',
                    category='gato'
                ),
                Product(
                    name='Eukanuba Razas Medianas',
                    description='Alimento premium para perros de raza mediana, 15kg.',
                    price=35000,
                    stock=7,
                    image_url='img/eukanuba.jpg',
                    category='perro'
                ),
                Product(
                    name='Cat Chow Gatitos',
                    description='Alimento para gatitos, 8kg.',
                    price=17000,
                    stock=10,
                    image_url='img/catchow.jpg',
                    category='gato'
                )
            ]
            db.session.bulk_save_objects(productos)
            db.session.commit()
    # Ejecuta la app en modo desarrollo
    app.run(debug=True)
