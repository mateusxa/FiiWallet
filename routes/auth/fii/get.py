from app import app, db
from app.UserFIIs import UserFII
from app.FIIs import FIIs
from flask import jsonify
from authenticate import jwt_required


@app.route('/auth/fii')
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

