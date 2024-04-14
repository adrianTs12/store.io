from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import flash
from flask import g

from app import *

import os

#==============================================
# INICIALIZACION
#==============================================
@app.before_request
def before_request():
    if 'usuario' in session:
        g.usuario = session['usuario']
    else:
        g.usuario = None

#==============================================
# INICIO
#==============================================
@app.route('/')
def index():
    if g.usuario:
        return redirect(url_for('catalog_products'))
    else:
        return redirect(url_for('login'))

#==============================================
# INICIO DE SESION
#==============================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.contraseña == contraseña:
            session['usuario'] = usuario.nombre
            return redirect(url_for('index'))
        
        flash('Credenciales Incorrectas. Vuelva a intentarlo!', 'warning')        
        
    return render_template('login.html')

#==============================================
# REGISTRAR USUARIO
#==============================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        direccion = request.form['direccion']
        contraseña = request.form['contraseña']
        
        usuario_existente = Usuario.query.filter_by(nombre=nombre).first()
        if usuario_existente:
            flash('El nombre de usuario ya esta en uso. Porfavor intenta con otro!', 'warning')
        else:
            usuario = Usuario(nombre=nombre, email=email, direccion=direccion, contraseña=contraseña)
            db.session.add(usuario)
            db.session.commit()
            
            flash("Se registro con exito. Porfavor inicia sesion!", 'success')
            return redirect(url_for('login'))
        
    return render_template('signup.html')

#==============================================
# CERRAR SESION
#==============================================
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Cerraste sesion!', 'warning')
    return redirect(url_for('index'))

#==============================================
# CATALOGO DE PRODUCTOS
#==============================================
@app.route('/products')
def catalog_products():
    products = Producto.query.all()
    return render_template('products.html', productos=products)

#==============================================
# VER ARTICULO
#==============================================
@app.route('/products/<int:id>')
def view_product(id):
    articulo = Producto.query.filter_by(id=id).first()
        
    return render_template('product.html', articulo=articulo)

#==============================================
# CARRITO DE COMPRAS
#==============================================
@app.route('/cart')
def cart():
    carrito = Carrito.query.filter_by(cliente=g.usuario).all()
    precio_total = 0
    
    pendientes = []
    comprados = []
    
    precio_realizadas = 0
    precio_pendientes = 0

    for articulo in carrito:
        articulo_original = Producto.query.filter_by(nombre=articulo.articulo).first()

        if articulo.estado:
            comprados.append(articulo)
            precio_realizadas += articulo.precio
            continue

        if articulo.cantidad > articulo_original.cantidad:
            articulo.cantidad = articulo_original.cantidad
            articulo.precio = articulo_original.precio * articulo.cantidad
            
        if not articulo.cantidad > 0:
            articulo.precio = 0
        
        pendientes.append(articulo)
        precio_pendientes += articulo.precio
        

    return render_template('cart.html', total_pendientes=precio_pendientes, total_realizadas=precio_realizadas, productos_pendientes=pendientes, productos_comprados=comprados, precio_total=precio_total)

#==============================================
# COMPRAR CARRITO DE COMPRAS
#==============================================
@app.route('/cart/buy')
def cart_buy():
    # Guardamos los articulos del carrrito del usuario
    articulos = Carrito.query.filter_by(cliente=g.usuario).all()
    
    compra_realizada = False
    
    for articulo in articulos:
        if articulo.estado:
            continue
        
        articulo_original = Producto.query.filter_by(nombre=articulo.articulo).first()
        
        if articulo.cantidad > articulo_original.cantidad:
            continue
        
        articulo_original.cantidad -= articulo.cantidad
        
        pedido = Pedido(
            cliente = g.usuario,
            articulo = articulo.articulo,
            cantidad = articulo.cantidad,
            precio_total = articulo.precio
        )
                
        articulo.estado = True
        
        db.session.add(pedido)
        db.session.commit()
        
        compra_realizada = True
    
    if compra_realizada:      
        usuario = Usuario.query.filter_by(nombre=g.usuario).first()
        msg = Message('Gracias por tu compra!', recipients=[usuario.email], sender=app.config['MAIL_USERNAME'])
        msg.body = '''Gracias por tu pedido, el encargo estara en camino!'''
        mail.send(msg)
        
        flash('Se realizo tu compra!', 'success')
    else:
        flash("No se pudo realizar tu compra!", 'warning')

    return redirect(url_for('cart'))

#==============================================
# AGREGAR PRODUCTO AL CARRITO
#==============================================
@app.route('/cart/add/<int:id>', methods=['POST'])
def cart_add_product(id):
    articulo = Producto.query.filter_by(id=id).first()
    
    if not(articulo.cantidad > 0):
        flash("No esta disponible este articulo!", 'warning')
        return redirect(url_for('catalog_products'))
    
    cantidad = int(request.form['cantidad'])
    precio = articulo.precio * cantidad
    
    if articulo:
        carrito = Carrito(cliente = g.usuario, articulo = articulo.nombre, cantidad = cantidad, precio = precio, imagen = articulo.imagen)
        db.session.add(carrito)
        db.session.commit()
        
        flash("Articulo guardado!", 'success')
        return redirect(url_for('cart'))
    
    return redirect(url_for('catalog_products'))

#==============================================
# ELIMINAR PRODUCTO DEL CARRITO
#==============================================
@app.route('/cart/delete/<int:id>')
def cart_delete_product(id):
    articulo = Carrito.query.filter_by(id=id).first()
    if articulo:
        db.session.delete(articulo)
        db.session.commit()
        flash("Articulo eliminado!", 'success')
        
    return redirect(url_for('cart'))

#==============================================
# AYUDA
#==============================================
@app.route('/help')
def help():
    return render_template('help.html')


#==============================================
# PANEL DE CONTROL - ADMIN
#==============================================
@app.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

#==============================================
# AGREGAR NUEVO PRODUCTO - ADMIN
#==============================================
@app.route('/dashboard/add/product', methods=['GET', 'POST'])
def dashboard_add_product():
    if request.method == 'POST':
        imagen = request.files['imagen']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        try:
            id = db.session.query(db.func.max(Producto.id)).scalar() + 1
        except:
            id = 1
            
        filename = f'{id}.png'
        dirfileupload = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagen.save(dirfileupload)
        
        dirfile = f'/static/articulos/{id}.png'
        
        nuevo_producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad, imagen=dirfile)
        db.session.add(nuevo_producto)
        db.session.commit()
        
        flash('Articulo agregado con exito!', 'success')
        return redirect(url_for('dashboard'))
        
        
    return render_template('admin/add_product.html')

#==============================================
# TABLA DE PRODUCTOS - ADMIN
#==============================================
@app.route('/dashboard/products')
def dashboard_list_products():
    productos = Producto.query.all()
    return render_template('admin/list_products.html', productos = productos)

#==============================================
# ELIMINAR PRODUCTO DE LA TABLA - ADMIN
#==============================================
@app.route('/dashboard/products/delete/<int:id>')
def dashboard_delete_product(id):
    product = Producto.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Articulo eliminado de la tabla!', 'success')
        
    return redirect(url_for('dashboard_list_products'))
    
#==============================================
# EDITAR PRODUCTO DE LA TABLA - ADMIN
#==============================================
@app.route('/dashboard/products/edit/<int:id>', methods=['GET', "POST"])
def dashboard_edit_product(id):
    producto = Producto.query.filter_by(id=id).first()
    if request.method == 'POST':
        imagen = request.files['imagen']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        if imagen:
            filename = f'{producto.id}.png'
            dirfileupload = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            os.remove(dirfileupload)
            
            imagen.save(dirfileupload)
        
        producto.nombre = nombre
        producto.cantidad = cantidad
        producto.precio = precio
        
        db.session.commit()
        flash('El articulo fue actualizado!', 'success')
        
        return redirect(url_for('dashboard_list_products'))
    
    return render_template('admin/edit_product.html', producto=producto)
        
#==============================================
# TABLA DE PEDIDOS - ADMIN
#==============================================
@app.route('/dashboard/pedidos')
def dashboard_list_pedidos():
    pedidos = Pedido.query.all()
    return render_template('admin/list_pedidos.html', pedidos = pedidos)

#==============================================
# TABLA DE USUUARIOS - ADMIN
#==============================================
@app.route('/dashboard/users')
def dashboard_list_users():
    usuario = Usuario.query.all()
    return render_template('admin/list_users.html', usuarios = usuario)