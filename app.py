from flask import Flask
from src.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from src.models import db
from src.schemas import ma
from src.routes import bp_materia_prima, bp_proveedor, bp_compra, bp_producto, bp_pedido

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp_materia_prima)
    app.register_blueprint(bp_proveedor)
    app.register_blueprint(bp_compra)
    app.register_blueprint(bp_producto)
    app.register_blueprint(bp_pedido)

    @app.route('/', methods=['GET'])
    def index():
        return {'message': 'Bienvenido a la API de Materias Primas de Sushi Store'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)