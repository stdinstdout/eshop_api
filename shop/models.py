from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime


from .database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(31), unique=True)
    items = relationship("ShopItem", back_populates="category", cascade="all, delete")


class ShopItem(Base):
    __tablename__ = 'shop_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(63))
    price = Column(Float)
    added_time = Column(DateTime)
    updated_time = Column(DateTime)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="items")
