# app.py
# Punto de entrada de la aplicación Flask para el portal de ventas online
# Aquí se configuran las rutas principales y la inicialización de la app

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from models import db, Product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cambia_esto_por_una_clave_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- ADMINISTRACIÓN DE PRODUCTOS ---
@app.route('/admin')
def admin():
    products = Product.query.order_by(Product.id).all()
    return render_template('admin.html', products=products)

@app.route('/admin/update_product', methods=['POST'])
def admin_update_product():
    data = request.get_json()
    product = Product.query.get(int(data['id']))
    if not product:
        return jsonify({'success': False, 'msg': 'Producto no encontrado'})
    product.name = data['name']
    try:
        product.price = float(data['price'])
    except Exception:
        product.price = 0.0
    try:
        product.stock = int(data['stock'])
    except Exception:
        product.stock = 0
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/delete_product', methods=['POST'])
def admin_delete_product():
    data = request.get_json()
    product = Product.query.get(int(data['id']))
    if not product:
        return jsonify({'success': False, 'msg': 'Producto no encontrado'})
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/add_product', methods=['POST'])
def admin_add_product():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'msg': 'Nombre requerido'})
    try:
        price = float(data.get('price', 0))
    except Exception:
        price = 0.0
    try:
        stock = int(data.get('stock', 0))
    except Exception:
        stock = 0
    product = Product(name=name, price=price, stock=stock, category='perro')
    db.session.add(product)
    db.session.commit()
    return jsonify({'success': True})



@app.route('/')
def index():
    # Mostrar todos los productos activos para clientes
    products = Product.query.order_by(Product.id).all()
    # Para productos destacados, puedes filtrar por algún criterio o mostrar los primeros N
    featured_products = products[:6] if len(products) > 6 else products
    return render_template('index.html', products=products, featured_products=featured_products)


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


# --- ADMINISTRACIÓN DE ARTÍCULOS (CRUD) ---
from flask import abort

@app.route('/admin/articulos')
def admin_articulos():
    productos = Product.query.order_by(Product.id).all()
    return render_template('admin_articulos.html', productos=productos)

@app.route('/admin/articulos/add', methods=['GET', 'POST'])
def admin_add_articulo():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        try:
            price = float(price)
        except Exception:
            price = 0.0
        stock = request.form.get('stock', 0)
        try:
            stock = int(stock)
        except Exception:
            stock = 0
        category = request.form.get('category', 'perro')
        image_url = None
        image = request.files.get('image')
        if image and image.filename:
            from werkzeug.utils import secure_filename
            filename = secure_filename(image.filename)
            img_folder = os.path.join('static', 'img', 'productos')
            os.makedirs(img_folder, exist_ok=True)
            img_path = os.path.join(img_folder, filename)
            image.save(img_path)
            image_url = os.path.join('img', 'productos', filename)
        if not name:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('admin_add_articulo'))
        producto = Product(name=name, price=price, stock=stock, category=category, image_url=image_url)
        db.session.add(producto)
        db.session.commit()
        flash('Artículo agregado correctamente', 'success')
        return redirect(url_for('admin_articulos'))
    return render_template('form_articulo.html', modo='agregar')

@app.route('/admin/articulos/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_articulo(id):
    producto = Product.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        try:
            price = float(price)
        except Exception:
            price = 0.0
        stock = request.form.get('stock', 0)
        try:
            stock = int(stock)
        except Exception:
            stock = 0
        category = request.form.get('category', 'perro')
        image = request.files.get('image')
        if image and image.filename:
            from werkzeug.utils import secure_filename
            filename = secure_filename(image.filename)
            img_folder = os.path.join('static', 'img', 'productos')
            os.makedirs(img_folder, exist_ok=True)
            img_path = os.path.join(img_folder, filename)
            image.save(img_path)
            producto.image_url = os.path.join('img', 'productos', filename)
        if not name:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('admin_edit_articulo', id=id))
        producto.name = name
        producto.price = price
        producto.stock = stock
        producto.category = category
        db.session.commit()
        flash('Artículo actualizado correctamente', 'success')
        return redirect(url_for('admin_articulos'))
    return render_template('form_articulo.html', modo='editar', producto=producto)

@app.route('/admin/articulos/delete/<int:id>', methods=['GET'])
def admin_delete_articulo(id):
    producto = Product.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Artículo eliminado correctamente', 'success')
    return redirect(url_for('admin_articulos'))

import pdfplumber
import re
import csv
from werkzeug.utils import secure_filename

@app.route('/admin/actualizar_precios', methods=['GET', 'POST'])
def admin_actualizar_precios():
    resumen = None
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No se subió ningún archivo.', 'danger')
            return redirect(request.url)
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            flash('Selecciona un archivo PDF.', 'danger')
            return redirect(request.url)
        filename = secure_filename(pdf_file.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        pdf_path = os.path.join(upload_folder, filename)
        pdf_file.save(pdf_path)
        # Extraer datos del PDF
        rows = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and any(cell and cell.strip() for cell in row):
                            rows.append([cell.strip() if cell else '' for cell in row])
        # Parsear precios
        def parse_precio(precio_str):
            if not precio_str:
                return None
            precio_str = precio_str.replace('$', '').replace('.', '').replace(',', '.').strip()
            try:
                return float(precio_str)
            except Exception:
                return None
        pares = []
        for row in rows:
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
        # Actualizar precios en la base
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
        # Guardar reporte de no encontrados
        reporte_path = os.path.join(upload_folder, 'reporte_no_encontrados.csv')
        with open(reporte_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre_pdf', 'precio_pdf'])
            for nombre, precio in no_encontrados:
                writer.writerow([nombre, precio])
        resumen = {
            'actualizados': actualizados,
            'no_encontrados': len(no_encontrados),
            'reporte_url': url_for('static', filename=f'uploads/reporte_no_encontrados.csv')
        }
        flash(f'Precios actualizados para {actualizados} productos. No encontrados: {len(no_encontrados)}', 'info')
    return render_template('admin_actualizar_precios.html', resumen=resumen)

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
