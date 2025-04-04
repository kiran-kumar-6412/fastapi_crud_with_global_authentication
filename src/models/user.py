from sqlalchemy import Column, String, Integer, Boolean
from .base import Base  # Ensure base.py contains declarative_base()

class User(Base):
    __tablename__ = "users"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(250), nullable=False)  # Ensure password cannot be NULL
    is_active = Column(Boolean, default=True)
    role= Column(String(100))

    # def __init__(self, email, username, is_active, role, password):
    #     self.email = email
    #     self.username = username
    #     self.is_active = is_active
    #     self.role = role
    #     self.password = password

