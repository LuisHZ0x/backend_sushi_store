from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# creacion de la tabla de materias primas en la base de datos

class Materia_prima(db.Model):
    __tablename__ = 'materia_prima'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad =  db.Column(db.Float, nullable=False)
    unidad_medida = db.Column(db.Enum('g', 'unidad'), nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)

# Creacion de la tabla proveedores en la base de datos
class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    material_proveido = db.Column(db.String(100), nullable=False)

# Tabla de compra de la materia prima
class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key=True)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)

# Tabla de productos
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen = db.Column(db.String(200), nullable=True)
    precio_venta = db.Column(db.Float, nullable=False)

# Tabla de materia prima en productos
class Materia_prima_producto(db.Model): #producto_materia segun el MER
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    Materia_prima_id = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=False)
    Producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

# tabla de detalles del pedido
class Detalles_pedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

# tabla pedidos
class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
