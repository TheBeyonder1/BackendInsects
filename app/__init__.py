from flask import Flask
from app.models import db
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes import register_routes

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    register_routes(app)

    return app
