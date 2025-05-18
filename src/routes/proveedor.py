from flask import Blueprint, request
from ..models import db, Proveedor
from ..schemas import ProveedorSchema

bp_proveedor = Blueprint('proveedor', __name__)

# Inicializar el esquema de proveedores
Proveedor_schema = ProveedorSchema()
Proveedores_schema = ProveedorSchema(many=True)

# ruta para agregar proveedores
@bp_proveedor.route('/proveedores', methods=['POST'])
def create_proveedor():
    data = request.get_json()
    new_proveedor = Proveedor(
        nombre=data['nombre'],
        telefono=data['telefono'],
        email=data['email'],
        direccion=data['direccion'],
        material_proveido=data['material_proveido']
    )
    db.session.add(new_proveedor)
    db.session.commit()
    return Proveedor_schema.jsonify(new_proveedor)

# ruta para obtener todos los proveedores
@bp_proveedor.route('/proveedores', methods=['GET'])
def get_proveedores():
    proveedores = Proveedor.query.all()
    return Proveedores_schema.jsonify(proveedores)

# ruta para actualizar un proveedor
@bp_proveedor.route('/proveedores/<int:id>', methods=['PUT'])
def update_proveedor(id):
    data = request.get_json()
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return {'message': 'Proveedor no encontrado'}, 404

    proveedor.nombre = data['nombre']
    proveedor.telefono = data['telefono']
    proveedor.email = data['email']
    proveedor.direccion = data['direccion']
    proveedor.material_proveido = data['material_proveido']

    db.session.commit()
    return Proveedor_schema.jsonify(proveedor)

# ruta para eliminar un proveedor
@bp_proveedor.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return {'message': 'Proveedor no encontrado'}, 404

    db.session.delete(proveedor)
    db.session.commit()
    return {'message': 'Proveedor eliminado'}