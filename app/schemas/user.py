"""
User schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt
from app.utils.utils import password_regex


class UserID(BaseModel):
    """
    Class for User Auth based on Pydantic Base Model.
    """
    id: PositiveInt = Field(..., title='ID', description='ID of the User')


class UserBasic(BaseModel):
    """
    Class for UserBasic based on Pydantic Base Model.
    """
    username: str = Field(
        ..., title='Username',
        description='Username to identify the user', min_length=4,
        max_length=15)
    email: EmailStr = Field(
        ..., title='Email',
        description='Preferred e-mail address of the User')


class UserPassword(BaseModel):
    """
    User class for its password based on Pydantic Base Model.
    """
    password: str = Field(
        default=..., title='Password', min_length=8, max_length=14,
        description='Password of the User', regex=password_regex)


class UserAuth(UserBasic, UserID):
    """
    Class for User Auth that inherits from UserBasic and UserID.
    """


class UserCreate(UserPassword, UserBasic):
    """
    User base class that inherits from UserPassword and UserBasic.
    """

    class Config:
        """
        Config class for User
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U"
            }
        }


class UserCreateSuper(UserPassword, UserBasic):
    """
    User base class that inherits from UserPassword and UserBasic.
    """
    is_superuser: bool = Field(
        default=True, title='Is super user?',
        description='True if the user is super user; otherwise false')

    class Config:
        """
        Config class for User
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "is_superuser": True
            }
        }


class UserValidation(BaseModel):
    """
    Class for User attributes that are automatically created in the
     database based on Pydantic Base Model.
    """
    is_superuser: bool = Field(
        default=False, title='Is super user?',
        description='True if the user is super user; otherwise false')
    is_active: bool = Field(
        default=True, title='Is active?',
        description='True if the user is active; otherwise false')


class UserInDB(UserValidation):
    """
    User in DB that inherits from UserValidation.
    """
    created_at: datetime = Field(
        default_factory=datetime.now, title='Created at',
        description='Time the User was created')
    updated_at: Optional[datetime] = Field(
        default=None, title='Updated at',
        description='Time the User was updated')


class User(UserInDB, UserCreate, UserID):
    """
    Request class for creating User that inherits from UserInDB,
     UserCreate and UserID.
    """

    class Config:
        """
        Config class for User
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "is_superuser": False,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }


class UserCreateResponse(UserValidation, UserAuth):
    """
    Response class for creating User that inherits from UserInDB and
     UserAuth.
    """

    class Config:
        """
        Config class for UserResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "is_superuser": False,
                "is_active": True
            }
        }


class UserResponse(UserInDB, UserAuth):
    """
    Response class for User that inherits from UserInDB and UserAuth.
    """

    class Config:
        """
        Config class for UserResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "is_superuser": False,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }


class UserUpdate(BaseModel):
    """
    Request class for updating User based on Pydantic Base Model.
    """
    username: Optional[str] = Field(
        default=None, title='Username',
        description='Username to identify the user',
        min_length=4, max_length=15)
    email: Optional[EmailStr] = Field(
        default=None, title='Email',
        description='Preferred e-mail address of the User')
    password: Optional[str] = Field(
        default=None, title='New Password', min_length=8, max_length=14,
        description='New Password of the User', regex=password_regex)

    class Config:
        """
        Config class for UserUpdate
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U"
            }
        }


class UserNewPassword(BaseModel):
    """
    User New Password class that inherits from Pydantic Base Model.
    """
    password: str = Field(
        ..., title='Hashed Password', min_length=40,
        description='Hashed Password of the User')


class UserUpdateResponse(UserInDB, UserNewPassword, UserAuth):
    """
    Response class for updating User that inherits from UserInDB,
     UserPassword and UserAuth.
    """

    class Config:
        """
        Config class for UserUpdateResponse
        """
        orm_mode: bool = True
        schema_extra: dict[str, dict] = {
            "example": {
                "id": 1,
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*Hk7pH9*35Fu&3UHk7pH9*35Fu&3U35Fu&3U",
                "is_active": True,
                "is_superuser": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
