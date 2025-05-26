from app.backend.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True)

    tasks = relationship('Tasks', back_populates='user')

from sqlalchemy.schema import CreateTable
print(CreateTable(Users.__table__))