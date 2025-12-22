from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuration CORS stricte pour 127.0.0.1
    CORS(app,
         resources={r"/*": {"origins": ["http://127.0.0.1:4200", "http://localhost:4200"]}},
         supports_credentials=True)

    # Import des routes
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app