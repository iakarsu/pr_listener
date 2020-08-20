from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.types import DateTime
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

Base = declarative_base()
db_string = os.getenv("DB_STRING")
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)
session = Session()

class PRTable(Base):
    __tablename__ = 'PRTable'

    id = Column(Integer, primary_key=True)
    link = Column(String(240))
    title = Column(String(240))
    date = Column(String(240))

    def __repr__(self):
        return f"Title('{self.title}', 'Date('{self.date}')"

Base.metadata.bind = engine
def db_create():
    Base.metadata.create_all()

