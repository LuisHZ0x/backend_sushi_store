from flask import Blueprint, request
from ..models import db, Producto
from ..schemas import ProductoSchema

bp_producto = Blueprint('productos', __name__)

# Inicializar el esquema de productos
Producto_schema = ProductoSchema()
Productos_schema = ProductoSchema(many=True)

# Ruta para crear un nuevo producto
@bp_producto.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    new_producto = Producto(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        imagen=data['imagen'],
        precio_venta=data['precio_venta'],
    )
    db.session.add(new_producto)
    db.session.commit()
    return Producto_schema.jsonify(new_producto)

# Ruta para obtener todos los productos
@bp_producto.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return Productos_schema.jsonify(productos)

# Ruta para actualizar un producto existente
@bp_producto.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    producto = Producto.query.get_or_404(id)
    producto.nombre = data['nombre']
    producto.descripcion = data['descripcion']
    producto.imagen = data['imagen']
    producto.precio_venta = data['precio_venta']
    db.session.commit()
    return Producto_schema.jsonify(producto)

# Ruta para eliminar un producto existente
@bp_producto.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return '', 204