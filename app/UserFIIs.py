from app import db, ma


class UserFII(db.Model):
    __tablename__ = 'user_fii'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String(84), nullable=False)
    fii_code = db.Column(db.String(84), nullable=False)
    created = db.Column(db.DateTime)

    def __init__(self, user_id, fii_code, created):
        self.user_id = user_id
        self.fii_code = fii_code
        self.created = created

    def __repr__(self):
        return f"<User : {self.user_id}, {self.fii_code}, {self.created} >"


class UserFIISchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'fii_code', 'created')


user_fii_share_schema = UserFIISchema()
user_fiis_share_schema = UserFIISchema(many=True)
