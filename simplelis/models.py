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
    first_name = Column('first_name', String(128), nullable=False)
    last_name = Column('last_name', String(128), nullable=False)
    email = Column('email', String(128), nullable=True)
    gender = Column('gender', String(8), nullable=False)
    birthdate = Column('birthdate', Date(), nullable=False)
    orders = relationship('Order', backref='patient')


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column('order_id', String(16), primary_key=True)
    orderdate = Column('order_date', Date, nullable=False)
    ordertime = Column('order_time', Time, nullable=False)
    doctor = Column('doctor', String(128))
    labs = relationship('Lab', backref='order')
    patient_id = Column(String(16), ForeignKey('patients.id'))


class Lab(Base):
    __tablename__ = 'labs'
    lab_id = Column('lab_id', String(16), primary_key=True)
    recv_date = Column('recv_date', Date, nullable=False)
    recv_time = Column('recv_time', Time, nullable=False)
    report_date = Column('report_date', Date)
    report_time = Column('report_time', Time)
    results = Column('results', Numeric())
    test_id = Column(String(16), ForeignKey('tests.test_code'))
    order_id = Column(String(16), ForeignKey('orders.order_id'))


class Test(Base):
    __tablename__ = 'tests'
    test_code = Column('test_code', String(8), primary_key=True)
    name = Column('name', String(255), nullable=False)
    unit = Column('unit', String(16))
    labs = relationship('Lab', backref='test')
