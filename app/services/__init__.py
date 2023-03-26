"""
Services initialization package
"""
from typing import TypeVar, Union, Optional
from app.models.user import User
from app.schemas.student import StudentResponse, StudentCreateResponse, \
    StudentUpdateResponse
from app.schemas.user import UserResponse, UserUpdateResponse, User as \
    UserCreate

T = TypeVar('T', StudentResponse, StudentCreateResponse, UserCreate,
            StudentUpdateResponse, UserResponse, UserUpdateResponse)


async def model_to_response(
        model: Union[User], response_model: T) -> Optional[T]:
    """
    Converts a User object to a Pydantic response model
    :param model: Object from Pydantic Base Model class
    :type model: User or Model
    :param response_model: Response model
    :type response_model: T
    :return: Model inherited from SQLAlchemy Declarative Base
    :rtype: T
    """
    if not model:
        return None
    return response_model.from_orm(model)
