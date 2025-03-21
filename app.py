from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.models import db
from app.routes import register_routes  # 👈 Importas función que registra los blueprints

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
register_routes(app)  # 👈 Aquí se registran los endpoints desde Blueprints

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
