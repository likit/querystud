import os
import glob
import pandas as pd
from datetime import datetime, timedelta
from random import randint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Patient, Test, Order, Lab

data_dir = 'datafiles'

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
engine = create_engine('postgres+psycopg2://postgres:{}@pg/simplelis'.
                       format(POSTGRES_PASSWORD))
Session = sessionmaker(bind=engine)
session = Session()

def parse_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')


def parse_time(timestr):
    return datetime.strptime(timestr, '%I:%M %p')


def load_patient():
    for f in glob.glob(os.path.join(data_dir, 'patient?.csv')):
        df = pd.read_csv(f)
        for ix,row in df.iterrows():
            pnt = Patient(
                first_name=row['first_name'],
                last_name=row['last_name'],
                id=row['id'],
                email=row['email'],
                gender=row['gender'],
                birthdate=parse_date(row['birthdate'])
            )
            session.add(pnt)
        session.commit()


def load_test():
    for f in glob.glob(os.path.join(data_dir, 'test*.csv')):
        df = pd.read_csv(f)
        for ix,row in df.iterrows():
            test = Test(
                test_code=row['testCode'],
                name=row['name'],
                unit=row['unit']
            )
            session.add(test)
        session.commit()


def load_order():
    tests = ['ldl']
    for t in tests:
        for f in glob.glob(os.path.join(data_dir, '{}*.csv'.format(t))):
            df = pd.read_csv(f)
            for ix,row in df.iterrows():
                order = session.query(Order).filter(Order.order_id==row['orderid']).first()
                if order:
                    print(order.order_id)
                test = session.query(Test).filter(Test.test_code==row['testid']).first()
                orderDateTime = datetime.strptime('{} {}'.format(
                    row['orderdate'],
                    row['ordertime']
                ), '%m/%d/%Y %I:%M %p')
                recvDateTime = orderDateTime + timedelta(minutes=randint(10,50))
                reportDateTime = recvDateTime + timedelta(minutes=randint(10,50))
                lab = Lab(
                    lab_id=row['labid'],
                    test_id=test.test_code,
                    recv_date=recvDateTime.date(),
                    recv_time=recvDateTime.time(),
                    report_date=reportDateTime.date(),
                    report_time=reportDateTime.time(),
                    results=str(row['results']),
                )
                if not order:
                    order = Order(
                        order_id=row['orderid'],
                        orderdate=parse_date(row['orderdate']),
                        ordertime=parse_time(row['ordertime']),
                        doctor=row['doctor'],
                    )
                order.labs.append(lab)
                session.add(lab)
                session.add(order)
            session.commit()

def add_order_to_patient():
    patients = list(session.query(Patient))
    for order in session.query(Order):
        idx = randint(0,len(patients)-1)
        patient = patients[idx]
        patient.orders.append(order)
        session.add(patient)
    session.commit()


if __name__ == '__main__':
    load_patient()
    load_test()
    load_order()
    add_order_to_patient()
