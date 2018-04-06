from enum import IntEnum

from project import db
from project.models.delivery_address import DeliveryAddress
from project.models.order_item import OrderItem


class OrderStatus(IntEnum):
    PENDING = 0
    AWAITING_PAYMENT = 1
    AWAITING_SHIPMENT = 2
    COMPLETED = 3
    CANCELLED = 4


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    items = db.relationship('OrderItem', backref='order', lazy=True)
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('delivery_addresses.id'), nullable=False)
    delivery_address = db.relationship('DeliveryAddress')
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=True)

    def __init__(self, delivery_address: DeliveryAddress, user_id: int = None):
        self.user_id = user_id
        self.delivery_address_id = delivery_address.id
