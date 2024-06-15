# middleware.py

from flask import request, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from connection import session

from models import Users  # Import model User

# Middleware function untuk memeriksa user sebelum masuk ke endpoint tertentu
def check_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verifikasi keberadaan JWT dalam request
        # check if header Authorization is present
        if not request.headers.get('Authorization'):
            return jsonify({'message': 'Silahkan Login Terlebih dahulu'}), 400
        
        # check if token is valid
        verify_jwt_in_request()

        # Dapatkan user_id dari JWT
        user_id = get_jwt_identity()

        # Query user dari database (contoh menggunakan SQLAlchemy)
        user = session.query(Users).filter(Users.id == user_id).first()

        # Tambahkan informasi user ke request context jika ditemukan
        if user:
            # setattr(request, 'current_user', user)
            return fn(*args, **kwargs)
        else:
            return jsonify({'message': 'User not found'}), 404

    return wrapper
