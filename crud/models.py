from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from crud.database import DeclarativeBase


class Passwords(DeclarativeBase):
    """
    Класс для создания объектов типа password и добавления их в БД
    """
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_name = Column('app_name', String, unique=True)
    password = Column('password', String)
    keys = relationship("Keys", cascade="all, delete")

    def __repr__(self):
        return f"id={self.id}, app_name={self.app_name}, password={self.password}"


class Keys(DeclarativeBase):
    """
    Класс для создания объектов типа key и добавления их в БД
    """
    __tablename__ = "p_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column('p_key', String)
    password_id = Column(Integer, ForeignKey('passwords.id'))
    password = relationship("Passwords", cascade="all, delete")



# class AppKeys(DeclarativeBase):
#     """
#     Класс для создания объектов типа app_key и добавления их в БД
#     """
#     __tablename__ = "a_keys"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     key = Column('a_key', String)
#     app_id = Column(Integer, ForeignKey('passwords.id'))
#     app = relationship("Passwords", cascade="all, delete")

#
# class Order(Base):
#     __tablename__ = "order"
#
#     items = relationship("Item", cascade="all, delete-orphan")
#     customer = relationship("User", cascade="save-update")
#
# class Item(Base):
#     __tablename__ = "item"
#
#     order = relationship(
#         "Order", backref=backref("items", cascade="all, delete-orphan")
#     )
