"""
User model script
"""
from datetime import datetime
from pydantic import EmailStr, PositiveInt
from sqlalchemy import Column, Integer, String, CheckConstraint, text, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP
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
    is_active: bool = Column(
        Boolean(), default=True, nullable=False, server_default=text("true"),
        comment='True if the user is active; otherwise false')
    is_superuser: bool = Column(
        Boolean(), default=False, nullable=False, server_default=text("false"),
        comment='True if the user is super user; otherwise false')
    created_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"), comment='Time the User was created')
    updated_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        nullable=True, comment='Time the User was updated')

    __table_args__ = (
        CheckConstraint(settings.EMAIL_CONSTRAINT, name='email_format'),
    )
