from sqlalchemy import Column, Integer, String, Date

from db import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    additional_data = Column(String(250))