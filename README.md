<<<<<<< HEAD
# Portal de Ventas Online - Base

Este proyecto es una base para un portal de ventas online, desarrollado con Flask y SQLite. Está pensado para ser fácil de entender, expandir y personalizar.

## Estructura del Proyecto
- `app.py`: Punto de entrada de la aplicación. Configura Flask, rutas principales y la inicialización de la base de datos. Cada función y sección está comentada para que entiendas su propósito.
- `models.py`: Define los modelos de datos (Usuario, Producto, Pedido). Incluye métodos para gestión segura de contraseñas y relaciones básicas.
- `requirements.txt`: Dependencias necesarias para ejecutar el proyecto (Flask, Flask-Login, Flask-SQLAlchemy, Werkzeug).
- `templates/`: Carpeta donde se encuentran las vistas HTML. Incluye archivos para el catálogo, login, registro y carrito de compras, todos con comentarios explicativos.
- `static/style.css`: Estilos básicos para el sitio, fácilmente personalizables.

## ¿Cómo ejecutar el proyecto?
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
3. Abre tu navegador en [http://localhost:5000](http://localhost:5000)

## Funcionalidades incluidas
- Catálogo de productos (index)
- Registro e inicio de sesión de usuarios
- Carrito de compras (por sesión)
- Finalización de compra (muy básica)
- Estructura lista para expandir con administración, historial de pedidos, etc.

## Comentarios en el código
Cada archivo, función y etiqueta HTML contiene comentarios explicativos en español, para que puedas aprender y modificar fácilmente el proyecto.
=======
# tienda
>>>>>>> a6432b0e1ff26465a35b2ffdce754c2d9a82dab9
