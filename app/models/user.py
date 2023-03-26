"""
User model script
"""
from pydantic import EmailStr, PositiveInt
from sqlalchemy import Column, Integer, String, CheckConstraint
from app.db.base_class import Base
from ..core.config import settings


class User(Base):
    """
    User class model as a table
    """
    __tablename__ = "users"

    id: PositiveInt = Column(
        Integer, index=True, unique=True, nullable=False, primary_key=True,
        comment='ID of the User')
    username: str = Column(
        String(15), CheckConstraint('char_length(username) >= 4'),
        unique=True, nullable=False, comment='Username to identify the user')
    email: EmailStr = Column(
        String(320), CheckConstraint('char_length(email) >= 3'),
        unique=True, nullable=False,
        comment='Preferred e-mail address of the User')
    password: str = Column(
        String(100), nullable=False, comment='Hashed password of the User')

    __table_args__ = (
        CheckConstraint(settings.EMAIL_CONSTRAINT, name='email_format'),
    )
