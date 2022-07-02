from flask import jsonify

def is_type(value, tpe):

    if isinstance(value, tpe):
        return
    else:
        return jsonify({
            "errorCode": "0000",
            "errorMessage": "Fii code must be an string"
        }), 400