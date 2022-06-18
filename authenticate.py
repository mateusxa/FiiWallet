from functools import wraps

import jwt
from flask import request, jsonify, current_app

from app.Users import User


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({"error": "voce nao tem permissao para acessar essa rota."}), 403

        if not "Bearer" in token:
            return jsonify({"error": "token invalido."}), 401
        try:
            token_pure = token.replace("Bearer ", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(decoded['id'])
        except:
            return jsonify({"error": "token invalido"})

        return f(current_user=current_user, *args, **kwargs)

    return wrapper
