from sqlalchemy import and_
from app import app, db
from app.UserFIIs import UserFII, user_fii_share_schema
from app.FIIs import FIIs
from flask import jsonify, request
from authenticate import jwt_required
from utils.check import is_type

import datetime
import utils.fii as Fii_Data

@app.route('/auth/fii', methods=["POST"])
@jwt_required
def register_fiis(current_user):
    fii_code_request = request.json['fii_code']
    quantity_request = request.json['quantity']

    is_type(quantity_request, int)
    if not isinstance(quantity_request, int):
        return jsonify({
            "errorCode": "0000",
            "errorMessage": "Quantity must be an integer"
        }), 400
        
    if not isinstance(fii_code_request, str):
        return jsonify({
            "errorCode": "0000",
            "errorMessage": "Fii code must be an string"
        }), 400

    fii = FIIs.query.filter_by(fii_code=fii_code_request).first()

    if fii is None:
        stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, month_prof, \
            patrimonial_value, p_vp = Fii_Data.get_fii_data(fii_code_request)

        fii = FIIs(fii_code_request, stock_price, daily_liquidity, last_yield, dividend_yield,
                    liquid_assets, month_prof, patrimonial_value, p_vp)

        db.session.add(fii)

        user_fii = UserFII(current_user.id, fii_code_request, quantity_request)
    
        db.session.add(user_fii)

        db.session.commit()
    else:
        user_fii = UserFII.query.filter(and_(UserFII.user_id == current_user.id, UserFII.fii_code==fii_code_request)).first()
        
        if user_fii is None:
            user_fii = UserFII(
                current_user.id,
                fii_code_request,
                quantity_request
            )

            db.session.add(user_fii)
        else:
            user_fii.quantity += quantity_request

        db.session.commit()



    result = user_fii_share_schema.dump(
        UserFII.query.filter(and_(UserFII.user_id == current_user.id, UserFII.fii_code==fii_code_request)).first()
    )

    return jsonify(result)


