from flask import Blueprint, request
from ..models import db, Pedido, Materia_prima
from ..schemas import PedidoSchema

bp_pedido = Blueprint('pedido', __name__)