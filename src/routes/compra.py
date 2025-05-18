from flask import Blueprint, request
from ..models import db, Compra, Materia_prima
from ..schemas import CompraSchema

bp_compra = Blueprint('compra', __name__)

# Inicializar el esquema de compras
Compra_schema = CompraSchema()
Compras_schema = CompraSchema(many=True)

# Ruta para crear una nueva compra
@bp_compra.route('/compras', methods=['POST'])
def create_compra():
    data = request.get_json()
    cantidad_comprada = data.get('cantidad', 0)
    materia_prima_id = data['materia_prima_id']

    # Buscar la materia prima correspondiente
    materia_prima = Materia_prima.query.get(materia_prima_id)
    if not materia_prima:
        return {'message': 'Materia prima no encontrada'}, 404

    # Sumar la cantidad comprada
    materia_prima.cantidad += cantidad_comprada

    # Registrar la compra
    new_compra = Compra(
        materia_prima_id=materia_prima_id,
        proveedor_id=data['proveedor_id'],
        cantidad=cantidad_comprada
    )
    db.session.add(new_compra)
    db.session.commit()
    return Compra_schema.jsonify(new_compra)

# Ruta para obtener todas las compras
@bp_compra.route('/compras', methods=['GET'])
def get_compras():
    compras = Compra.query.all()
    return Compras_schema.jsonify(compras)