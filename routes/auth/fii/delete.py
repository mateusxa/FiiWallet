from sqlalchemy import table
from app import app, db
from app.UserFIIs import UserFII, user_fii_share_schema
from flask import jsonify, request
from authenticate import jwt_required

@app.route('/auth/fii', methods=["DELETE"])
@jwt_required
def delete_fiis(current_user):
    fii_code_request = request.json['fii_code']
    quantity_request = request.json['quantity']

    # for _ in range(quantity_request):

    obj = UserFII.query.filter(UserFII.fii_code==fii_code_request and UserFII.user_id == current_user.id).first() #.order_by(UserFII.user_id.desc()).first()  #.first()
    db.session.delete(obj)
    db.session.commit()


    result = {
        "tickect_qtd": quantity_request,
        "ticket": "ticket"
    }

    return jsonify(result)