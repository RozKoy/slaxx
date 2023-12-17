from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(nullable=False)
    item_count: Mapped[int] = mapped_column(nullable=False)
    price_count: Mapped[int] = mapped_column(nullable=False)
    create_at: Mapped[str] = mapped_column(nullable=False)
    customerId: Mapped[int] = mapped_column(nullable=False)
