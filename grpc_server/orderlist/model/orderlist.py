from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Orderlist(Base):
    __tablename__ = "order_list"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_count: Mapped[int] = mapped_column(nullable=False)
    orderId: Mapped[int] = mapped_column(nullable=False)
    productId: Mapped[int] = mapped_column(nullable=False)
