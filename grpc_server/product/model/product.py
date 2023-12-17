from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price: Mapped[int] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    