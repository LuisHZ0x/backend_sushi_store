from flask import Blueprint, request
from ..models import db, Producto, Materia_prima, Materia_prima_producto
from ..schemas import MateriaPrimaSchema, ProductoSchema, MateriaPrimaProductoSchema
from datetime import datetime

bp_producto_materia = Blueprint('producto_materia', __name__)

# Inicializar el esquema de productos
Producto_schema = ProductoSchema()
Productos_schema = ProductoSchema(many=True)
# Inicializar el esquema de materias primas
Materia_prima_schema = MateriaPrimaSchema()
Materias_primas_schema = MateriaPrimaSchema(many=True)
# Inicializar el esquema de materias primas por producto
Materia_prima_producto_schema = MateriaPrimaProductoSchema()
Materias_primas_producto_schema = MateriaPrimaProductoSchema(many=True)

# Ruta para Descontar materia prima segun id de materia prima y id de producto
@bp_producto_materia.route('/descontar_mp', methods=['POST'])
def descontar_materia_prima():
    data = request.get_json()
    producto_id = data['producto_id']
    materia_prima_id = data['materia_prima_id']

    # Buscar la relación producto-materia prima
    relacion = Materia_prima_producto.query.filter_by(
        Producto_id=producto_id,
        Materia_prima_id=materia_prima_id
    ).first()

    if not relacion:
        return {'message': 'Relación producto-materia prima no encontrada'}, 404

    cantidad_a_descontar = relacion.cantidad

    # Buscar la materia prima real
    materia_prima = Materia_prima.query.get(materia_prima_id)
    if not materia_prima:
        return {'message': 'Materia prima no encontrada'}, 404

    # Verificar si hay suficiente cantidad
    if materia_prima.cantidad < cantidad_a_descontar:
        return {'message': 'No hay suficiente materia prima disponible'}, 400

    # Descontar la cantidad registrada en la relación
    materia_prima.cantidad -= cantidad_a_descontar
    db.session.commit()

    return Materia_prima_schema.jsonify(materia_prima)

# Ruta para asociar una materia prima a un producto
@bp_producto_materia.route('/asociar_mp', methods=['POST'])
def asociar_materia_prima_a_producto():
    data = request.get_json()
    producto_id = data['producto_id']
    materia_prima_id = data['materia_prima_id']
    cantidad = data['cantidad']

    nueva_relacion = Materia_prima_producto(
        Producto_id=producto_id,
        Materia_prima_id=materia_prima_id,
        cantidad=cantidad
    )
    db.session.add(nueva_relacion)
    db.session.commit()
    return Materia_prima_producto_schema.jsonify(nueva_relacion), 201

# Ruta para obtener todas las materias primas de un producto
@bp_producto_materia.route('/productos/<int:producto_id>/materias_primas', methods=['GET'])
def get_materias_primas_producto(producto_id):
    # Obtener el producto
    producto = Producto.query.get(producto_id)
    if not producto:
        return {'message': 'Producto no encontrado'}, 404

    # Obtener las materias primas asociadas al producto
    materias_primas = Materia_prima_producto.query.filter_by(Producto_id=producto_id).all()
    return Materias_primas_producto_schema.jsonify(materias_primas)



