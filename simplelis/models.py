import os

from sqlalchemy import (Column, Integer, String, Numeric,
                            Date, Time, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column('id', String(16), primary_key=True)
    first_name = Column('firstName', String(128), nullable=False)
    last_name = Column('lastName', String(128), nullable=False)
    email = Column('email', String(128), nullable=True)
    gender = Column('gender', String(8), nullable=False)
    birthdate = Column('birthdate', Date(), nullable=False)
    orders = relationship('Order', backref='patient')


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column('orderId', String(16), primary_key=True)
    orderdate = Column('orderDate', Date, nullable=False)
    ordertime = Column('orderTime', Time, nullable=False)
    doctor = Column('doctor', String(128))
    labs = relationship('Lab', backref='order')


class Lab(Base):
    __tablename__ = 'labs'
    lab_id = Column('labId', String(16), primary_key=True)
    test_id = Column(String(16), ForeignKey('tests.testCode'))
    recvDate = Column('recvDate', Date, nullable=False)
    recvTime = Column('recvTime', Time, nullable=False)
    reportDate = Column('recvDate', Date)
    reportTime = Column('recvTime', Time)
    results = Column('results', Numeric())
    test = relationship('Test', backref=backref('lab', uselist=False))


class Test(Base):
    __tablename__ = 'tests'
    test_code = Column('testCode', String(8), primary_key=True)
    name = Column('name', String(255), nullable=False)
    unit = Column('unit', String(16))
