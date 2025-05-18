from flask import Blueprint, request
from datetime import datetime
from ..models import db, Materia_prima
from ..schemas import MateriaPrimaSchema

bp_materia_prima = Blueprint('materia_prima', __name__)

# Inicializar el esquema de materias primas
Materia_prima_schema = MateriaPrimaSchema()
Materias_primas_schema = MateriaPrimaSchema(many=True)

# Ruta para crear una nueva materia prima
@bp_materia_prima.route('/mp', methods=['POST'])
def create_materia_prima():
    data = request.get_json()
    fecha_vencimiento = datetime.strptime(data['fecha_vencimiento'], "%Y-%m-%d").date()
    new_materia_prima = Materia_prima(
        nombre=data['nombre'],
        cantidad=data['cantidad'],
        unidad_medida=data['unidad_medida'],
        fecha_vencimiento=fecha_vencimiento,
        costo_unitario=data['costo_unitario'],
        imagen=data['imagen']
    )
    db.session.add(new_materia_prima)
    db.session.commit()
    return Materia_prima_schema.jsonify(new_materia_prima)

    # Ruta para obtener todas las materias primas
@bp_materia_prima.route('/mp', methods=['GET'])
def get_materias_primas():
    materias_primas = Materia_prima.query.all()
    return Materias_primas_schema.jsonify(materias_primas)

    # Ruta para obtener una materia prima por nombre
@bp_materia_prima.route('/mp/<nombre>', methods=['GET'])
def get_materia_prima(nombre):
    materia_prima = Materia_prima.query.filter_by(nombre=nombre).first()
    if materia_prima:
        return Materia_prima_schema.jsonify(materia_prima)
    else:
        return {'message': 'Materia prima no encontrada'}, 404
    
    # Ruta para actualizar una materia prima
@bp_materia_prima.route('/mp/<int:id>', methods=['PUT'])
def update_materia_prima(id):
    data = request.get_json()
    materia_prima = Materia_prima.query.get(id)
    if not materia_prima:
        return {'message': 'Materia prima no encontrada'}, 404

    materia_prima.nombre = data['nombre']
    materia_prima.cantidad = data['cantidad']
    materia_prima.unidad_medida = data['unidad_medida']
    materia_prima.fecha_vencimiento = datetime.strptime(data['fecha_vencimiento'], "%Y-%m-%d").date()
    materia_prima.costo_unitario = data['costo_unitario']
    materia_prima.imagen = data['imagen']

    db.session.commit()
    return Materia_prima_schema.jsonify(materia_prima)

    # Ruta para eliminar una materia prima
@bp_materia_prima.route('/mp/<int:id>', methods=['DELETE'])
def delete_materia_prima(id):
    materia_prima = Materia_prima.query.get(id)
    if not materia_prima:
        return {'message': 'Materia prima no encontrada'}, 404

    db.session.delete(materia_prima)
    db.session.commit()
    return {'message': 'Materia prima eliminada'}