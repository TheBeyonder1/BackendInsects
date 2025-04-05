from flask import Blueprint, request, jsonify
from app.models import db, Post, Comment, Like, User

posts_bp = Blueprint('posts', __name__)




@posts_bp.route('/posts', methods=['POST'])
def crear_post():
    data = request.json
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nuevo_post = Post(
        user_id=data['user_id'],
        image_url=data['image_url'],
        description=data.get('description', ''),
        latitude=data.get('latitude'),       # <- opcional
        longitude=data.get('longitude')      # <- opcional
    )
    
    db.session.add(nuevo_post)
    db.session.commit()
    
    return jsonify({"mensaje": "Post creado", "post_id": nuevo_post.id}), 201



# 🔹 Obtener todos los Posts
@posts_bp.route('/posts', methods=['GET'])
def obtener_posts():
    user_id = request.args.get('user_id')  # Obtener el ID del usuario actual desde Unity

    posts = Post.query.order_by(Post.id.desc()).all()
    resultados = []
    for post in posts:
        ya_le_dio_like = False
        if user_id:
            like = Like.query.filter_by(post_id=post.id, user_id=user_id).first()
            ya_le_dio_like = like is not None

        resultados.append({
            'id': post.id,
            'user_id': post.user_id,
            'username': post.user.username if post.user else "Desconocido",
            'image_url': post.image_url,
            'description': post.description,
            'created_at': post.created_at.isoformat() if post.created_at else None,
            'latitude': post.latitude,
            'longitude': post.longitude,
            'total_likes': Like.query.filter_by(post_id=post.id).count(),
            'total_comments': Comment.query.filter_by(post_id=post.id).count(),
            'likes': 1 if ya_le_dio_like else 0  # 👈 Este campo indica si el usuario ya dio like
        })

    return jsonify(resultados), 200


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



# 🔹 Obtener comentarios de un Post
@posts_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def obtener_comentarios(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post no encontrado"}), 404

    comentarios = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    
    resultado = []
    for c in comentarios:
        resultado.append({
            "id": c.id,
            "user_id": c.user_id,
            "username": c.user.username if c.user else "Desconocido",
            "text": c.text,
            "created_at": c.created_at.isoformat() if c.created_at else None
        })

    return jsonify(resultado), 200
