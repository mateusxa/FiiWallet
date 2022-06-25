import scripts.fii as Fii_Data
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app import app, db
from app.FIIs import FIIs, fii_share_schema


@app.route('/fiis/register', methods=['POST'])
def fiis_register():
    fii_code = request.json['fii_code']
    stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, patrimonial_value, \
    month_prof, p_vp = Fii_Data.get_fii_data(fii_code)

    for _ in range(3):
        try:
            fii = FIIs(fii_code, stock_price, daily_liquidity, last_yield, dividend_yield,
                    liquid_assets, month_prof, patrimonial_value, p_vp)

            db.session.add(fii)
            db.session.commit()

            result = fii_share_schema.dump(
                FIIs.query.filter_by(fii_code=fii_code).first()
            )
            

            return jsonify(result)
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
