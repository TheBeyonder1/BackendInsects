from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
