from typing import List

from sqlalchemy import desc
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from project import db
from project.models.delivery_address import DeliveryAddress
from project.models.order import Order, OrderStatus
from project.models.order_item import OrderItem
from project.models.user import User

session: Session = db.session


def get(order_id: int) -> Order:
    return Order.query.filter_by(id=order_id).first()


def get_all() -> List[Order]:
    return Order.query.all()


def get_last_order() -> Order:
    return Order.query.order_by(desc(Order.created)).first()


def get_last_by_user(user: User) -> Order:
    return Order.query.filter_by(user_id=user.id).order_by(desc(Order.created)).first()


def add(items: List[OrderItem], delivery_address: DeliveryAddress, user_id: int = None) -> Order:
    session.add(delivery_address)
    session.flush([delivery_address])

    order = Order(delivery_address, user_id)
    total = sum([item.price * item.count for item in items])
    order.total = total
    session.add(order)

    order.items.extend(items)

    session.commit()

    return order


def add_item(order: Order, item: OrderItem):
    order.items.append(item)
    session.commit()


def change_status(order: Order, status: OrderStatus):
    order.status = status
    try:
        session.commit()
    except StatementError:
        return False

    return True


def cancel(order: Order):
    order.status = OrderStatus.CANCELLED
    session.commit()
