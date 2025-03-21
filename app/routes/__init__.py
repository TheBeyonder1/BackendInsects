from flask import Blueprint

# Importa los blueprints individuales
from .predict import predict_bp

def register_routes(app):
    app.register_blueprint(predict_bp)
