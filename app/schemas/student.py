"""
Student schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, PositiveInt, validator
from app.schemas.grimoire import Grimoire
from app.schemas.magic_affinity import MagicAffinity
from app.schemas.user import UserCreate, UserResponse, User, UserCreateResponse
from app.utils.utils import generate_grimoire


class StudentID(BaseModel):
    """
    Core class for Student based on Pydantic Base Model.
    """
    id: PositiveInt = Field(..., title='ID', description='ID of the Student')


class StudentBase(BaseModel):
    """
    Student request class based on Pydantic Base Model.
    """
    first_name: str = Field(
        ..., title='First name', description='First name(s) of the Student',
        max_length=20)
    last_name: str = Field(
        ..., title='Last name', description='Last name(s) of the Student',
        max_length=20)
    identification: str = Field(
        ..., title='Identification',
        description='Alphanumeric Identification of max 10 characters',
        max_length=10, regex='^[a-zA-Z0-9]{1,10}$')
    age: PositiveInt = Field(
        ..., title='Age', description='Age of the Student')
    magic_affinity: MagicAffinity = Field(
        default=MagicAffinity.LIGHT, title='MagicAffinity',
        description='Magic affinity of the student')

    @validator('age')
    def validate_age(cls, age: PositiveInt) -> PositiveInt:
        """
        Validate age for only two digits maximum
        :param age: The age of the Student
        :type age: PositiveInt
        :return: The age validated or ValueError
        :rtype: PositiveInt
        """
        if age > 99:
            raise ValueError('Age must be less than or equal to 99')
        return age


class StudentCreate(StudentBase):
    """
    Student Create class that inherits from StudentBase.
    """
    user: UserCreate = Field(
        ..., title='User Create', description='User basic information')

    class Config:
        """
        Config class for StudentCreate
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "identification": "12ab34cd5e",
                "age": 17,
                "magic_affinity": MagicAffinity.WIND,
                "user": {
                    "username": "yuno123",
                    "email": "yuno_grinberryall@mail.com",
                    "password": "Password1.-"
                }
            }
        }


class StudentApproved(StudentBase):
    """
    Student approved request class that inherits from StudentBase.
    """
    grimoire: Grimoire = Field(
        default_factory=generate_grimoire, title='Grimoire',
        description='Random Grimoire assigned to the student')


class StudentInDB(BaseModel):
    """
    Class for Student attributes that are automatically created in the
     database based on Pydantic Base Model.
    """
    created_at: datetime = Field(
        default_factory=datetime.now, title='Created at',
        description='Time the Student was created')
    updated_at: Optional[datetime] = Field(
        default=None, title='Updated at',
        description='Time the Student was updated')


class Student(StudentInDB, StudentApproved, StudentID):
    """
    Student class that inherits from StudentInDB, StudentApproved and
     StudentID.
    """
    user: User = Field(
        ..., title='User', description='User basic information')

    class Config:
        """
        Config class for Student
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "identification": "12ab34cd5e",
                "age": 17,
                "magic_affinity": MagicAffinity.WIND,
                "grimoire": Grimoire.GOOD_FORTUNE,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "user": {
                    "id": 1,
                    "username": "yuno123",
                    "email": "yuno_grinberryall@mail.com",
                    "password": "Password1.-",
                    "is_superuser": False,
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        }


class StudentResponse(StudentInDB, StudentApproved, StudentID):
    """
    Class for Student Response that inherits from StudentInDB,
     StudentApproved and StudentID.
    """
    user: UserResponse = Field(
        ..., title='User Response', description='User basic information')

    class Config:
        """
        Config class for StudentResponse
        """
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "identification": "12ab34cd5e",
                "age": 17,
                "magic_affinity": MagicAffinity.WIND,
                "grimoire": Grimoire.GOOD_FORTUNE,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "user": {
                    "id": 1,
                    "username": "yuno123",
                    "email": "yuno_grinberryall@mail.com",
                    "is_superuser": False,
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        }


class StudentCreateResponse(StudentCreate):
    """
    Response class for creating Student that inherits from
     StudentCreate.
    """
    user: UserCreateResponse = Field(
        ..., title='User Response', description='User basic information')

    class Config:
        """
        Config class for StudentCreateResponse
        """
        orm_mode: bool = True
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Yuno",
                "last_name": "Grinberryall",
                "identification": "12ab34cd5e",
                "age": 17,
                "magic_affinity": MagicAffinity.WIND,
                "user": {
                    "id": 1,
                    "username": "yuno123",
                    "email": "yuno_grinberryall@mail.com",
                    "is_superuser": False,
                    "is_active": True
                }
            }
        }


class StudentUpdate(BaseModel):
    """
    Request class for updating Student based on Pydantic Base Model.
    """
    first_name: Optional[str] = Field(
        default=None, title='First name',
        description='First name(s) of the Student', max_length=20)
    last_name: Optional[str] = Field(
        default=None, title='Last name',
        description='Last name(s) of the Student', max_length=20)
    identification: Optional[str] = Field(
        default=None, title='Identification',
        description='Alphanumeric Identification of max 10 characters',
        max_length=10, regex='^[a-zA-Z0-9]{1,10}$')
    age: Optional[PositiveInt] = Field(
        default=None, title='Age', description='Age of the Student')
    magic_affinity: Optional[MagicAffinity] = Field(
        default=None, title='MagicAffinity',
        description='Magic affinity of the student')

    @validator('age')
    def validate_age(cls, age: PositiveInt) -> PositiveInt:
        """
        Validate age for only two digits maximum
        :param age: The age of the Student
        :type age: PositiveInt
        :return: The age validated or ValueError
        :rtype: PositiveInt
        """
        if age > 99:
            raise ValueError('Age must be less than or equal to 99')
        return age

    class Config:
        """
        Config class for StudentUpdate
        """
        schema_extra: dict[str, dict] = {
            "example": {
                "first_name": "Asta",
                "last_name": "Staria",
                "identification": "09zy87xw6v",
                "age": 15,
                "magic_affinity": None
            }
        }
