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
    productos = data['productos']  # Espera una lista de dicts: [{'producto_id': 1, 'cantidad': 2}, ...]
    total = 0

    nuevo_pedido = Pedidos(
        fecha=datetime.now(),
        total=0  # Se actualizará después
    )
    db.session.add(nuevo_pedido)
    db.session.flush()  # Para obtener el id del pedido

    for item in productos:
        producto_id = item['producto_id']
        cantidad_producto = item['cantidad']
        producto = Producto.query.get(producto_id)
        if not producto:
            db.session.rollback()
            return jsonify({'error': f'Producto con id {producto_id} no encontrado'}), 404

        subtotal = producto.precio_venta * cantidad_producto
        total += subtotal

        # Crear detalle de pedido
        detalle = Detalles_pedido(
            cantidad=cantidad_producto,
            subtotal=subtotal,
            pedido_id=nuevo_pedido.id,
            producto_id=producto_id
        )
        db.session.add(detalle)

        # Descontar materia prima
        materias_primas = Materia_prima_producto.query.filter_by(Producto_id=producto_id).all()
        for mp in materias_primas:
            materia = Materia_prima.query.get(mp.Materia_prima_id)
            if materia:
                cantidad_a_descontar = mp.cantidad * cantidad_producto
                if materia.cantidad < cantidad_a_descontar:
                    db.session.rollback()
                    return jsonify({'error': f'No hay suficiente {materia.nombre} para el producto {producto.nombre}'}), 400
                materia.cantidad -= cantidad_a_descontar

    nuevo_pedido.total = total
    db.session.commit()
    return pedido_schema.jsonify(nuevo_pedido)