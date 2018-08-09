import os
import glob
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Patient

data_dir = 'datafiles'

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
engine = create_engine('postgres+psycopg2://postgres:{}@pg/simplelis'.
                       format(POSTGRES_PASSWORD))
Session = sessionmaker(bind=engine)
session = Session()

def load_patient():
    for f in glob.glob(os.path.join(data_dir, 'patient?.csv')):
        df = pd.read_csv(f)
        for ix,row in df.iterrows():
            birthdate = datetime.strptime(row['birthdate'], '%m/%d/%Y')
            pnt = Patient(
                first_name=row['first_name'],
                last_name=row['last_name'],
                id=row['id'],
                email=row['email'],
                gender=row['gender'],
                birthdate=birthdate
            )
            session.add(pnt)
        session.commit()


if __name__ == '__main__':
    load_patient()
