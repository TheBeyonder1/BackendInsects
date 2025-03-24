# app/routes/test.py
from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"mensaje": "Todo está funcionando bien 🚀"})
