import json
from operator import and_
from sqlalchemy import desc, null
import scripts.fii as Fii_Data
from flask import jsonify, request
import datetime

import datetime
import jwt

from app import app, db
from app.UserFIIs import UserFII, user_fii_share_schema
from app.Users import User, user_share_schema
from app.FIIs import FIIs, fii_share_schema
from authenticate import jwt_required


@app.route('/auth/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

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

    return jsonify(result)


@app.route('/auth/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first_or_404()

    if not user.verify_password(password):
        return jsonify({
            "error": "suas credenciais estao erradas!"
        }), 403

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({"token": token})


@app.route('/auth/fiis/all')
@jwt_required
def get_fiis(current_user):

    db_query_list = db.session.query(UserFII.fii_code, db.func.count(UserFII.user_id)).filter(UserFII.user_id == current_user.id).group_by(UserFII.fii_code).all()

    result_list = []

    for db_query in db_query_list:

        fii_code = db_query[0]
        tickect_qtd = db_query[1]

        fii_code_query = FIIs.query.filter_by(fii_code=fii_code).first()

        d = {
            'fii_code': fii_code_query.fii_code,
            'stock_price': fii_code_query.stock_price,
            'daily_liquidity': fii_code_query.daily_liquidity,
            'last_yield': fii_code_query.last_yield,
            'dividend_yield': fii_code_query.dividend_yield,
            'liquid_assets': fii_code_query.liquid_assets,
            'month_prof': fii_code_query.month_prof,
            'patrimonial_value': fii_code_query.patrimonial_value,
            'p_vp': fii_code_query.p_vp,
            'tickect_qtd': tickect_qtd,
        }
        
        result_list.append(d)

    return jsonify(result_list)


@app.route('/auth/fiis', methods=["POST"])
@jwt_required
def register_fiis(current_user):
    fii_code_request = request.json['fii_code']
    quantity_request = request.json['quantity']
    date = datetime.datetime.utcnow()
    fii = FIIs.query.filter_by(fii_code=fii_code_request).first()

    if fii is None:
        stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, month_prof, \
            patrimonial_value, p_vp = Fii_Data.get_fii_data(fii_code_request)

        fii = FIIs(fii_code_request, stock_price, daily_liquidity, last_yield, dividend_yield,
                    liquid_assets, month_prof, patrimonial_value, p_vp)

        db.session.add(fii)

    for _ in range(quantity_request):
        user_fii = UserFII(current_user.id, fii_code_request, date)
    
        db.session.add(user_fii)

        db.session.commit()

    ticket = user_fii_share_schema.dump(
        UserFII.query.filter(UserFII.user_id == current_user.id and UserFII.fii_code==fii_code_request and UserFII.created==date).first()
    )

    result = {
        "tickect_qtd": quantity_request,
        "ticket": ticket
    }

    return jsonify(result)


@app.route('/auth/fiis', methods=["DELETE"])
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
