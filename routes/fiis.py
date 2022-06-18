import scripts.fii as Fii_Data
from flask import jsonify, request

from app import app, db
from app.FIIs import FIIs, fii_share_schema, fiis_share_schema
from authenticate import jwt_required


@app.route('/fiis/register', methods=['POST'])
def fiis_register():
    fii_code = request.json['fii_code']
    stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, month_prof, \
    patrimonial_value, p_vp = Fii_Data.get_fii_data(fii_code)

    fii = FIIs(fii_code, stock_price, daily_liquidity, last_yield, dividend_yield,
               liquid_assets, month_prof, patrimonial_value, p_vp)

    db.session.add(fii)
    db.session.commit()

    result = fii_share_schema.dump(
        FIIs.query.filter_by(fii_code=fii_code).first()
    )

    return jsonify(result)
