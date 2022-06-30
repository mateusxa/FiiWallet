from app import app, db
from sqlalchemy.exc import SQLAlchemyError
from app.Users import User
from flask import jsonify, request

import datetime
import jwt


@app.route('/auth/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    for _ in range(3):
        try:
            user = User.query.filter_by(email=email).first_or_404()
        
            if not user.verify_password(password):
                return jsonify({
                    "errorCode": "0000",
                    "errorMessage": "Invalid Credentials"
                }), 403

            payload = {
                "id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({"token": token})
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            error = error.lstrip("(").rstrip(")")

            error_code = error[0:4]

            if error_code == "2013":
                session_clear()
                pass
            else:
                payload = {
                    "errorCode": error_code,
                    "errorMessage": error[7:-1]
                }
                return jsonify(payload), 400

    return jsonify({
        "errorCode": "0000",
        "errorMessage": "Server may be down"
    })


@app.teardown_request
def session_clear(exception=None):
    db.session.remove()
    if exception and db.session.is_active:
        db.session.rollback()