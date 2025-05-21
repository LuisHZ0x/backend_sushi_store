from flask import Blueprint, request, jsonify
from ..models import db, Pedidos, Detalles_pedido, Producto, Materia_prima_producto, Materia_prima
from ..schemas import PedidosSchema
from datetime import datetime

bp_pedido = Blueprint('pedido', __name__)

# Inicializar el esquema de pedidos
pedido_schema = PedidosSchema()
pedidos_schema = PedidosSchema(many=True)

# Ruta para crear un nuevo pedido
@bp_pedido.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()
    fecha = datetime.now()
    total = 0

    # Crear un nuevo pedido
    nuevo_pedido = Pedidos(fecha=fecha, total=total)
    db.session.add(nuevo_pedido)
    db.session.commit()

    # Obtener el ID del nuevo pedido
    pedido_id = nuevo_pedido.id

    # Procesar los detalles del pedido
    for detalle in data['detalles']:
        producto_id = detalle['producto_id']
        cantidad = detalle['cantidad']

        # Obtener el producto y su precio de venta
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404

        subtotal = producto.precio_venta * cantidad
        total += subtotal

        # Crear un nuevo detalle de pedido
        nuevo_detalle = Detalles_pedido(cantidad=cantidad, subtotal=subtotal, pedido_id=pedido_id, producto_id=producto_id)
        db.session.add(nuevo_detalle)

    # Actualizar el total del pedido
    nuevo_pedido.total = total
    nuevo_pedido.fecha = fecha
    db.session.commit()

    return pedido_schema.jsonify(nuevo_pedido), 201

# Ruta para obtener los productos de un pedido
@bp_pedido.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    pedido = Pedidos.query.get(pedido_id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404

    detalles = Detalles_pedido.query.filter_by(pedido_id=pedido_id).all()
    detalles_data = []
    for detalle in detalles:
        producto = Producto.query.get(detalle.producto_id)
        detalles_data.append({
            'precio_venta': producto.precio_venta if producto else None,
            'cantidad': detalle.cantidad,
            'subtotal': detalle.subtotal,
            'nombre_producto': producto.nombre if producto else None
        })

    return jsonify({
        'fecha': pedido.fecha,
        'total': pedido.total,
        'detalles': detalles_data
    }), 200