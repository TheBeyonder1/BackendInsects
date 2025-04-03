from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email ya registrado"}), 400

    nuevo_usuario = User(
        username=data['username'],
        email=data['email']
    )
    nuevo_usuario.set_password(data['password'])  # Asegúrate de usar 'password' en el JSON
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = User.query.filter_by(email=data['email']).first()

    if usuario and usuario.check_password(data['password']):
        token = create_access_token(identity=usuario.id)
        return jsonify({
            "token": token,
            "user_id": usuario.id,
            "nombre": usuario.username,
            "email": usuario.email
        }), 200

    return jsonify({"error": "Credenciales inválidas"}), 401


@users_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()
    usuario = User.query.get(user_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "nombre": usuario.nombre,
        "email": usuario.email
    })
