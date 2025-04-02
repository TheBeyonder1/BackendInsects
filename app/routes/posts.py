from flask import Blueprint, request, jsonify
from app.models import db, Post, Comment, Like, User

posts_bp = Blueprint('posts', __name__)

# 🔹 Crear un Post
@posts_bp.route('/posts', methods=['POST'])
def crear_post():
    data = request.json
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nuevo_post = Post(user_id=data['user_id'], image_url=data['image_url'], description=data.get('description', ''))
    db.session.add(nuevo_post)
    db.session.commit()
    return jsonify({"mensaje": "Post creado", "post_id": nuevo_post.id}), 201

# 🔹 Editar un Post
@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
def editar_post(post_id):
    data = request.json
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post no encontrado"}), 404

    post.image_url = data.get('image_url', post.image_url)
    post.description = data.get('description', post.description)
    db.session.commit()
    return jsonify({"mensaje": "Post actualizado"}), 200

# 🔹 Eliminar un Post
@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def eliminar_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post no encontrado"}), 404

    # Eliminar los comentarios y likes relacionados
    Comment.query.filter_by(post_id=post_id).delete()
    Like.query.filter_by(post_id=post_id).delete()
    db.session.delete(post)
    db.session.commit()
    return jsonify({"mensaje": "Post eliminado"}), 200

# 🔹 Agregar un Comentario
@posts_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def agregar_comentario(post_id):
    data = request.json
    user = User.query.get(data['user_id'])
    post = Post.query.get(post_id)

    if not user or not post:
        return jsonify({"error": "Usuario o Post no encontrado"}), 404

    nuevo_comentario = Comment(user_id=data['user_id'], post_id=post_id, text=data['text'])
    db.session.add(nuevo_comentario)
    db.session.commit()
    return jsonify({"mensaje": "Comentario agregado", "comentario_id": nuevo_comentario.id}), 201

# 🔹 Eliminar un Comentario
@posts_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def eliminar_comentario(comment_id):
    comentario = Comment.query.get(comment_id)

    if not comentario:
        return jsonify({"error": "Comentario no encontrado"}), 404

    db.session.delete(comentario)
    db.session.commit()
    return jsonify({"mensaje": "Comentario eliminado"}), 200

# 🔹 Dar Like a un Post
@posts_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def dar_like(post_id):
    data = request.json
    user = User.query.get(data['user_id'])
    post = Post.query.get(post_id)

    if not user or not post:
        return jsonify({"error": "Usuario o Post no encontrado"}), 404

    # Verificar si ya dio like
    like_existente = Like.query.filter_by(user_id=data['user_id'], post_id=post_id).first()
    if like_existente:
        return jsonify({"mensaje": "Ya has dado like a este post"}), 400

    nuevo_like = Like(user_id=data['user_id'], post_id=post_id)
    db.session.add(nuevo_like)
    db.session.commit()
    return jsonify({"mensaje": "Like agregado", "total_likes": Like.query.filter_by(post_id=post_id).count()}), 201

# 🔹 Quitar Like de un Post
@posts_bp.route('/posts/<int:post_id>/like', methods=['DELETE'])
def quitar_like(post_id):
    data = request.json
    like = Like.query.filter_by(user_id=data['user_id'], post_id=post_id).first()

    if not like:
        return jsonify({"error": "Like no encontrado"}), 404

    db.session.delete(like)
    db.session.commit()
    return jsonify({"mensaje": "Like eliminado", "total_likes": Like.query.filter_by(post_id=post_id).count()}), 200
