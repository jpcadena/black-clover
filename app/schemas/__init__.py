"""
Schemas initialization package
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .magic_affinity import MagicAffinity


class CommonUserToken(BaseModel):
    """
    Common fields for User and Token classes based on EditableData.
    """
    given_name: str = Field(
        title='First name',
        description='Given name(s) or first name(s) of the User', min_length=1,
        max_length=50)
    family_name: str = Field(
        title='Last name',
        description='Surname(s) or last name(s) of the User', min_length=1,
        max_length=50)
    magic_affinity: MagicAffinity = Field(
        default=MagicAffinity.LIGHT, title='MagicAffinity',
        description='MagicAffinity of the Student')
    updated_at: Optional[datetime] = Field(
        default=None, title='Updated at',
        description='Time the User information was last updated')
