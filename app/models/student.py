"""
Student model script
"""
from datetime import datetime
from pydantic import PositiveInt
from sqlalchemy import Boolean, Column, Integer, String, CheckConstraint,\
    text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
from .user import User
from ..core.config import settings
from ..schemas import MagicAffinity
from ..schemas.grimoire import Grimoire
from ..utils.utils import generate_unique_id


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
        String(10), default=generate_unique_id, index=True, unique=True,
        nullable=False, comment='Identification of the student')
    age: PositiveInt = Column(
        Integer, CheckConstraint("age > 0 AND age <= 99"), nullable=False,
        comment='Age of the Student')
    magic_affinity: MagicAffinity = Column(Enum(MagicAffinity), nullable=False)
    grimoire_cover: Grimoire = Column(Enum(Grimoire), nullable=False)
    is_active: bool = Column(
        Boolean(), default=True, nullable=False, server_default=text("true"),
        comment='True if the student is active; otherwise false')
    created_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        default=datetime.now(), nullable=False,
        server_default=text("now()"), comment='Time the student was created')
    updated_at: datetime = Column(
        TIMESTAMP(timezone=False, precision=settings.TS_PRECISION),
        nullable=True, comment='Time the student was updated')
