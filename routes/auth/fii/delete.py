from sqlalchemy import and_
from app import app, db
from app.UserFIIs import UserFII, user_fii_share_schema
from flask import jsonify, request
from authenticate import jwt_required

@app.route('/auth/fii', methods=["DELETE"])
@jwt_required
def delete_fiis(current_user):
    fii_code_request = request.json['fii_code']
    quantity_request = request.json['quantity']

    user_fii = UserFII.query.filter(and_(UserFII.user_id == current_user.id, UserFII.fii_code==fii_code_request)).first()
    
    if user_fii is None:
        return jsonify({
            "errorCode": "0000",
            "errorMessage": "Fii not found"
        }), 404
    else:
        if(user_fii.quantity - quantity_request < 0):
            return jsonify({
                "errorCode": "0000",
                "errorMessage": "Quantity informed is greater than database quantity"
            }), 400
        else:
            user_fii.quantity -= quantity_request
        
    db.session.commit()

    result = user_fii_share_schema.dump(
        UserFII.query.filter(and_(UserFII.user_id == current_user.id, UserFII.fii_code==fii_code_request)).first()
    )

    return jsonify(result)