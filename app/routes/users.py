from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email ya registrado"}), 400

    nuevo_User = User(
        nombre=data['nombre'],
        email=data['email']
    )
    nuevo_User.set_password(data['contraseña'])
    db.session.add(nuevo_User)
    db.session.commit()

    return jsonify({"mensaje": "User registrado correctamente"}), 201


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    User = User.query.filter_by(email=data['email']).first()

    if User and User.check_password(data['contraseña']):
        token = create_access_token(identity=User.id)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401


@users_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    User_id = get_jwt_identity()
    User = User.query.get(User_id)
    return jsonify({
        "nombre": User.nombre,
        "email": User.email
    })
