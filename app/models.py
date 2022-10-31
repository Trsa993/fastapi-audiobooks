from enum import unique
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    author = Column(String)
    path = Column(String, nullable=False)
    img = Column(String, nullable=False)