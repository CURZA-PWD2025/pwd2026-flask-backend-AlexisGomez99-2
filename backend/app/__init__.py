from dotenv import load_dotenv
from flask import Flask
from app.models import db
from app.config import config
from app.routes.user_routes import users
from app.routes.rol_routes import roles
from app.routes.categoria_routes import categorias
from app.routes.producto_routes import productos
from app.routes.proveedor_routes import proveedores
from app.routes.movimiento_stock_routes import movimientos_stock
from app.routes.auth_routes import auth_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

load_dotenv(override = True)
import os
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    app.register_blueprint(users,url_prefix='/users')
    app.register_blueprint(roles,url_prefix='/roles')
    app.register_blueprint(categorias,url_prefix='/categorias')
    app.register_blueprint(productos, url_prefix='/productos')
    app.register_blueprint(proveedores,url_prefix='/proveedores')
    app.register_blueprint(movimientos_stock,url_prefix='/movimientos')
    app.register_blueprint(auth_bp,url_prefix='/auth')
    
    @app.route('/')
    @app.route('/<nombre>')    
    def home(nombre = None):
        if (nombre == None):
            return f' <h1>Hola  desde programacion web dinamica 2026<h1>'
        return f'Hola {nombre} te saludamos desde programacion web dinamica 2026'

    @app.route('/saludo')
    def saludo():
        return f'Hola desde programacion web dinamica 2026 saludo'
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    return app
    