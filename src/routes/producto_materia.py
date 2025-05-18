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



