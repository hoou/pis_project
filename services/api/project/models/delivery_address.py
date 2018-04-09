from project import db


class DeliveryAddress(db.Model):
    __tablename__ = "delivery_addresses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    street = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)

    def __init__(self, first_name, last_name, phone, street, zip_code, city, country):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street = street
        self.zip_code = zip_code
        self.city = city
        self.country = country
