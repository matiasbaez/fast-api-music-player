from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary
from models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key=True, index=True)
    email = Column(VARCHAR(100))
    username = Column(VARCHAR(100))
    password = Column(LargeBinary)