from app.FIIs import FIIs
import utils.fii as Fii_Data
from app import db


def update_fii(value):

    fii_code = value
    stock_price, daily_liquidity, last_yield, dividend_yield, liquid_assets, patrimonial_value, \
    month_prof, p_vp = Fii_Data.get_fii_data(fii_code)

    update = FIIs.query.filter_by(fii_code=value).first()

    update.stock_price = stock_price,
    update.daily_liquidity = daily_liquidity, 
    update.last_yield = last_yield, 
    update.dividend_yield = dividend_yield,
    update.liquid_assets = liquid_assets, 
    update.month_prof = month_prof, 
    update.patrimonial_value = patrimonial_value, 
    update.p_vp = p_vp

    db.session.commit()

    # print("stock_price: ", stock_price)
    # print("daily_liquidity: ", daily_liquidity)
    # print("last_yield: ", last_yield)
    # print("dividend_yield: ", dividend_yield)
    # print("liquid_assets: ", liquid_assets)
    # print("month_prof: ", month_prof)
    # print("patrimonial_value: ", patrimonial_value)
    # print("p_vp: ", p_vp)


def update_all():
    rows = FIIs.query.all()

    for row in rows:
        update_fii(row.fii_code)