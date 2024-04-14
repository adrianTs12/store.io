from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    contraseña = db.Column(db.String(80))
    direccion = db.Column(db.String(100))
    email = db.Column(db.String(80))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25))
    precio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    imagen = db.Column(db.String(50))

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(50))
    articulo = db.Column(db.String(25))
    cantidad = db.Column(db.Integer)
    precio_total = db.Column(db.Integer)
    
class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(50))
    articulo = db.Column(db.String(25)) 
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(50))
    estado = db.Column(db.Boolean)
    