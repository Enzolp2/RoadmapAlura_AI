from flask import Flask
from .config import get_config
from .views import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Registrar blueprints
    app.register_blueprint(main_bp)

    # Inicializar API - Flask-restx
    from api import api
    api.init_app(app)


    return app