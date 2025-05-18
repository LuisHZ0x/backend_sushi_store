from flask import Blueprint, request
from ..models import db, Pedido, Materia_prima, Detalles_pedido
from ..schemas import PedidoSchema, DetallesPedidoSchema
from datetime import datetime

bp_detalles_pedido = Blueprint('detalles_pedido', __name__)
# Inicializar el esquema de detalles de pedidos
Detalles_pedido_schema = DetallesPedidoSchema()
Detalles_pedidos_schema = DetallesPedidoSchema(many=True)

# Ruta para crear un nuevo detalle de pedido
#@bp_detalles_pedido.route('/detalles_pedidos', methods=['POST'])
#def create_detalles_pedido():
