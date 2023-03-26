"""
User schema
"""
from pydantic import BaseModel, EmailStr, PositiveInt, Field
from app.utils.utils import password_regex


class User(BaseModel):
    """
    User class based on Pydantic Base Model.
    """
    id: PositiveInt = Field(..., title='ID', description='ID of the User')
    username: str = Field(
        ..., title='Username', description='Username to identify the user',
        min_length=4, max_length=15)
    email: EmailStr = Field(
        ..., title='Email', description='Preferred e-mail address of the User')
    password: str = Field(
        ..., title='Password', description='Password of the User',
        min_length=8, max_length=14, regex=password_regex)

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
                "password": "Hk7pH9*35Fu&3U"}}
