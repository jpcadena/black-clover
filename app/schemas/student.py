"""
Student schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt
from app.schemas.magic_affinity import MagicAffinity
from app.utils.utils import password_regex


class StudentID(BaseModel):
    """
    Core class for Student based on Pydantic Base Model.
    """
    id: PositiveInt = Field(..., title='ID', description='ID of the Student')


class StudentUpdatedAt(BaseModel):
    """
    UpdatedAt class for Student based on Pydantic Base Model.
    """
    updated_at: Optional[datetime] = Field(
        default=None, title='Updated at',
        description='Time the Student was updated')


class StudentBaseAuth(BaseModel):
    """
    Student Base Auth class based on Pydantic Base Model
    """
    username: str = Field(
        ..., title='Studentname',
        description='Studentname to identify the user', min_length=4,
        max_length=15)
    email: EmailStr = Field(
        ..., title='Email',
        description='Preferred e-mail address of the Student')


class StudentName(BaseModel):
    """
    Student class for names attributes based on Pydantic Base Model.
    """
    first_name: str = Field(
        ..., title='First name', description='First name(s) of the Student')
    last_name: str = Field(
        ..., title='Last name', description='Last name(s) of the Student')


class StudentBase(StudentName, StudentBaseAuth):
    """
    Base class for Student that inherits from StudentAuth.
    """


class StudentAuth(StudentBaseAuth, StudentID):
    """
    Student Auth that inherits from StudentID.
    """

    class Config:
        """
        Config class for StudentAuth
        """
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com"}}


class StudentOptional(BaseModel):
    """
    Student class with optional attributes based on Pydantic Base Model.
    """
    magic_affinity: MagicAffinity = Field(
        default=MagicAffinity.LIGHT, title='MagicAffinity',
        description='MagicAffinity of the student')


class StudentCreate(StudentOptional, StudentBase):
    """
    Request class for creating Student that inherits from StudentOptional
     and StudentBase.
    """
    password: str = Field(
        ..., title='Password', description='Password of the Student',
        min_length=8, max_length=14, regex=password_regex)

    class Config:
        """
        Config class for StudentCreate
        """
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "password": "Hk7pH9*35Fu&3U",
                "magic_affinity": MagicAffinity.LIGHT}}


class StudentSuperCreate(StudentCreate):
    """
    Class to create a super_user that inherits from StudentCreate.
    """
    is_superuser: bool = Field(
        default=True, title='Is super user?',
        description='True if the user is super user; otherwise false')

    class Config:
        """
        Config class for StudentSuperCreate
        """
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "password": "Hk7pH9*35Fu&3U",
                "magic_affinity": MagicAffinity.LIGHT,
                "is_superuser": True}}


class StudentCreateResponse(StudentBase, StudentID):
    """
    Response class for creating Student that inherits from StudentID and
     StudentBase.
    """

    class Config:
        """
        Config class for StudentCreateResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example"}}


class StudentUpdate(BaseModel):
    """
    Request class for updating Student based on Pydantic Base Model.
    """
    username: Optional[str] = Field(
        default=None, title='Studentname',
        description='Studentname to identify the user',
        min_length=4, max_length=15)
    email: Optional[EmailStr] = Field(
        default=None, title='Email',
        description='Preferred e-mail address of the Student')
    first_name: Optional[str] = Field(
        default=None, title='First name',
        description='First name(s) of the Student')
    last_name: str = Field(
        default=None, title='Last name',
        description='Last name(s) of the Student')
    password: Optional[str] = Field(
        default=None, title='New Password', min_length=8, max_length=14,
        description='New Password of the Student', regex=password_regex)
    magic_affinity: MagicAffinity = Field(
        default=MagicAffinity.LIGHT, title='MagicAffinity',
        description='MagicAffinity of the student')

    class Config:
        """
        Config class for StudentUpdate
        """
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "password": "Hk7pH9*35Fu&3U",
                "magic_affinity": MagicAffinity.LIGHT}}


class StudentInDB(StudentUpdatedAt, BaseModel):
    """
    Class for Student attributes that are automatically created in the
     database based on Pydantic Base Model.
    """
    is_active: bool = Field(
        ..., title='Is active?',
        description='True if the user is active; otherwise false')
    is_superuser: bool = Field(
        ..., title='Is super user?',
        description='True if the user is super user; otherwise false')
    created_at: datetime = Field(
        default_factory=datetime.now, title='Created at',
        description='Time the Student was created')


class StudentPassword(BaseModel):
    """
    Student Password class that inherits from Pydantic Base Model.
    """
    password: str = Field(
        ..., title='Hashed Password', min_length=40,
        description='Hashed Password of the Student')


class StudentUpdateResponse(StudentInDB, StudentOptional, StudentPassword,
                            StudentName, StudentAuth):
    """
    Response class for updating Student that inherits from StudentInDB,
     StudentOptional, StudentPassword, StudentName and StudentAuth.
    """

    class Config:
        """
        Config class for StudentUpdateResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "password": "Hk7pH9*Hk7pH9*35Fu&3UHk7pH9*35Fu&3U35Fu&3U",
                "magic_affinity": MagicAffinity.LIGHT,
                "is_active": True,
                "is_superuser": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()}}


class Student(StudentUpdatedAt, StudentOptional, StudentBase):
    """
    Student class that inherits from StudentUpdatedAt, StudentRelationship,
     StudentCreate and StudentID.
    """
    password: str = Field(
        ..., title='Hashed Password', min_length=40,
        description='Hashed Password of the Student')
    is_active: bool = Field(
        default=True, title='Is active?',
        description='True if the user is active; otherwise false')
    is_superuser: bool = Field(
        default=False, title='Is super user?',
        description='True if the user is super user; otherwise false')
    created_at: datetime = Field(
        default_factory=datetime.now, title='Created at',
        description='Time the Student was created')

    class Config:
        """
        Config class for Student
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "password": "Hk7pH9*Hk7pH9*35Fu&3UHk7pH9*35Fu&3U35Fu&3U",
                "magic_affinity": MagicAffinity.LIGHT,
                "is_active": True,
                "is_superuser": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()}}


class StudentResponse(StudentInDB, StudentOptional, StudentBase, StudentID):
    """
    Response for Student class that inherits from StudentRelationship,
     StudentInDB, StudentOptional, StudentCreateResponse.
    """

    class Config:
        """
        Config class for StudentResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "first_name": "Some",
                "last_name": "Example",
                "magic_affinity": MagicAffinity.LIGHT,
                "is_active": True,
                "is_superuser": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()}}
