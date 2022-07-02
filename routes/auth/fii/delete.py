from app import app, db
from app.UserFIIs import UserFII, user_fii_share_schema
from flask import jsonify, request
from authenticate import jwt_required

@app.route('/auth/fii', methods=["DELETE"])
@jwt_required
def delete_fiis(current_user):
    fii_code_request = request.json['fii_code']
    quantity_request = request.json['quantity']

    for _ in range(quantity_request):
        user_fii = UserFII.query.filter_by(fii_code=fii_code_request).delete()

        db.session.commit()

    ticket = user_fii_share_schema.dump(
        UserFII.query.filter(UserFII.user_id == current_user.id and UserFII.fii_code==fii_code_request).first()
    )

    result = {
        "tickect_qtd": quantity_request,
        "ticket": ticket
    }

    return jsonify(result)