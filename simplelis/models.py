import os

from sqlalchemy import (Table, Column, Integer, String, Numeric, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:{}@localhost:5435/simplelis'
                       .format(POSTGRES_PASSWORD))

class Patient(Base):
    __tablename__ = 'patients'
    id = Column('id', String(16), primary_key=True)
    first_name = Column('firstName', String(128), nullable=False)
    last_name = Column('lastName', String(128), nullable=False)
    email = Column('email', String(128), nullable=True)
    gender = Column('gender', String(8), nullable=False)
    birthdate = Column('birthdate', Date(), nullable=False)

Base.metadata.create_all(engine)
