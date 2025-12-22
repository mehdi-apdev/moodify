from flask import Flask
from flask_cors import CORS
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuration CORS
    CORS(app, resources={r"/*": {"origins": Config.FRONTEND_URL}}, supports_credentials=True)

    # Enregistrement des blueprints
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app