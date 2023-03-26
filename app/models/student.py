"""
Student model script
"""
from datetime import datetime
from pydantic import PositiveInt
from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer,\
    String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from .user import User
from ..core.config import settings
from ..schemas import MagicAffinity
from ..schemas.grimoire import Grimoire


class Student(Base):
    """
    Student class model as a table
    """
    __tablename__ = "students"

    id: PositiveInt = Column(
        Integer, index=True, unique=True, nullable=False, primary_key=True,
        comment='ID of the student')
    user_id: Mapped[PositiveInt] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False,
        comment='ID of the student')
    user: Mapped[[User]] = relationship(lazy="selectin")
    first_name: str = Column(
        String(20), nullable=False, comment='First name(s) of the student')
    last_name: str = Column(
        String(20), nullable=False, comment='Last name(s) of the student')
    identification: str = Column(
        String(10), index=True, unique=True, nullable=False,
        comment='Identification of the student')
    age: PositiveInt = Column(
        Integer, CheckConstraint("age > 0 AND age <= 99"), nullable=False,
        comment='Age of the Student')
    magic_affinity: MagicAffinity = Column(
        Enum(MagicAffinity), nullable=False,
        comment='Magic affinity of the student')
    grimoire: Grimoire = Column(
        Enum(Grimoire), nullable=False,
        comment='Grimoire cover of the student')
    created_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"),
        comment='Time the student was registered')
    updated_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        nullable=True, comment='Time the student information was updated')
