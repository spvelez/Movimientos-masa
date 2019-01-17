from sqlalchemy import Column, Integer, String
from masas.database import DbModel


class User(DbModel):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    login = Column(String(128))
    password = Column(String(256))
    name = Column(String(256))
    role = Column(Integer)
