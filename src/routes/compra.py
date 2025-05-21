from flask import Blueprint, request
from ..models import db, Compra, Materia_prima, Proveedor
from datetime import datetime
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

# Ruta para obtener todas las compras segun id
@bp_compra.route('/compras/<int:id>', methods=['GET'])
def get_compra(id):
    compra = Compra.query.get(id)
    if not compra:
        return {'message': 'Compra no encontrada'}, 404

    materia_prima = Materia_prima.query.get(compra.materia_prima_id)
    proveedor = Proveedor.query.get(compra.proveedor_id)

    if not materia_prima or not proveedor:
        return {'message': 'Materia prima o proveedor no encontrados'}, 404

    return {
        'compra': {
            'cantidad': compra.cantidad
        },
        'materia_prima': {
            'id': materia_prima.id,
            'nombre': materia_prima.nombre,
            'cantidad': materia_prima.cantidad,
            'unidad_medida': materia_prima.unidad_medida,
            'fecha_vencimiento': str(materia_prima.fecha_vencimiento),
            'costo_unitario': materia_prima.costo_unitario,
            'imagen': materia_prima.imagen
        },
        'proveedor': {
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'telefono': proveedor.telefono,
            'email': proveedor.email,
            'direccion': proveedor.direccion,
            'material_proveido': proveedor.material_proveido
        }
    }
# Ruta para obtener todas las compras y mostrar detalles de cada compra
@bp_compra.route('/compras', methods=['GET'])
def get_compras():
    compras = Compra.query.all()
    if not compras:
        return {'message': 'No hay compras registradas'}, 404

    compras_data = []
    for compra in compras:
        materia_prima = Materia_prima.query.get(compra.materia_prima_id)
        proveedor = Proveedor.query.get(compra.proveedor_id)

        if not materia_prima or not proveedor:
            continue

        compras_data.append({
            'id': compra.id,
            'cantidad': compra.cantidad,
            'materia_prima': {
                'id': materia_prima.id,
                'nombre': materia_prima.nombre,
                'cantidad': materia_prima.cantidad,
                'unidad_medida': materia_prima.unidad_medida,
                'fecha_vencimiento': str(materia_prima.fecha_vencimiento),
                'costo_unitario': materia_prima.costo_unitario,
                'imagen': materia_prima.imagen
            },
            'proveedor': {
                'id': proveedor.id,
                'nombre': proveedor.nombre,
                'telefono': proveedor.telefono,
                'email': proveedor.email,
                'direccion': proveedor.direccion,
                'material_proveido': proveedor.material_proveido
            }
        })

    return {'compras': compras_data}

