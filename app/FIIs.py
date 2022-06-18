from app import db, ma


class FIIs(db.Model):
    __tablename__ = 'fiis'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fii_code = db.Column(db.String(84), nullable=False, unique=True)
    stock_price = db.Column(db.Float, nullable=False)
    daily_liquidity = db.Column(db.Float, nullable=False)
    last_yield = db.Column(db.Float, nullable=False)
    dividend_yield = db.Column(db.Float, nullable=False)
    liquid_assets = db.Column(db.Float, nullable=False)
    month_prof = db.Column(db.Float, nullable=False)
    patrimonial_value = db.Column(db.Float, nullable=False)
    p_vp = db.Column(db.Float, nullable=False)

    def __init__(self, fii_code, stock_price, daily_liquidity, last_yield, dividend_yield, 
        liquid_assets, month_prof, patrimonial_value, p_vp):
        self.fii_code = fii_code
        self.stock_price = stock_price
        self.daily_liquidity = daily_liquidity
        self.last_yield = last_yield
        self.dividend_yield = dividend_yield
        self.liquid_assets = liquid_assets
        self.month_prof = month_prof
        self.patrimonial_value = patrimonial_value
        self.p_vp = p_vp

    def __repr__(self):
        return f"<FII : {self.fii_code} >"


class FIIsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fii_code', 'stock_price' 'daily_liquidity', 'last_yield', 'dividend_yield', 'liquid_assets',
        'month_prof', 'patrimonial_value', 'p_vp')


fii_share_schema = FIIsSchema()
fiis_share_schema = FIIsSchema(many=True)
