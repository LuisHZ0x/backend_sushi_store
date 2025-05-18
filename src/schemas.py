from flask_marshmallow import Marshmallow
from .models import Materia_prima, Proveedor, Compra, Producto, Detalles_pedido, Pedidos, Materia_prima_producto

ma = Marshmallow()

# Definicion del esquema de la tabla de materias primas
class MateriaPrimaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Materia_prima
        fields = ('id', 'nombre', 'cantidad', 'unidad_medida', 'fecha_vencimiento', 'costo_unitario', 'imagen')

#definicion del esquema de la tabla de proveedores
class ProveedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
        fields = ('id', 'nombre', 'telefono', 'email', 'direccion', 'material_proveido')

# Definicion del esquema de la tabla de compras
class CompraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Compra
        fields = ('id', 'materia_prima_id', 'proveedor_id')
        include_fk = True

# Definicion del esquema de la tabla de productos
class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion', 'imagen', 'precio_venta')

# Definicion del esquema de la tabla materia prima en productos
class MateriaPrimaProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Materia_prima_producto
        fields = ('id', 'cantidad', 'Materia_prima_id', 'Producto_id')
        include_fk = True

# Definicion del esquema de la tabla de detalles del pedido
class DetallesPedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Detalles_pedido
        fields = ('id', 'cantidad', 'subtotal', 'pedido_id', 'producto_id')
        include_fk = True

# Definicion del esquema de la tabla de pedidos
class PedidosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedidos
        fields = ('id', 'fecha', 'total')