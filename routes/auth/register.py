from app import app, db
from flask import jsonify, request
from app.Users import User, user_share_schema
from sqlalchemy.exc import SQLAlchemyError


@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    try:
        user = User(
            username,
            email,
            password
        )

        db.session.add(user)
        db.session.commit()

        result = user_share_schema.dump(
            User.query.filter_by(email=email).first()
        )

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error.lstrip("(").rstrip(")")

        payload = {
            "errorCode": error[0:4],
            "errorMessage": error[7:-1]
        }
        return jsonify(payload), 400

    return jsonify(result)