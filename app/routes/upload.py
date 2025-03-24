from flask import Blueprint, request, jsonify
from app.services.s3 import subir_imagen_a_s3
from werkzeug.utils import secure_filename
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    final_filename = f"{timestamp}_{filename}"

    try:
        url = subir_imagen_a_s3(file, final_filename)
        return jsonify({'message': 'File uploaded', 'url': url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
