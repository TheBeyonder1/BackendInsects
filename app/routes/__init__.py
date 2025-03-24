from flask import Blueprint
from app.routes.users import users_bp

# Importa los blueprints individuales
from .predict import predict_bp
from .test import test_bp
from .upload import upload_bp

def register_routes(app):
    app.register_blueprint(predict_bp)
    app.register_blueprint(users_bp, url_prefix='/api/usuarios')
    app.register_blueprint(test_bp, url_prefix="/api") 
    app.register_blueprint(upload_bp, url_prefix="/api")




   
