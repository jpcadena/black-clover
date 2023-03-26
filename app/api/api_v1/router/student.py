"""
Student API Router
"""
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status, \
    Response
from fastapi.params import Query, Path
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import CurrentUser
from app.core.security.exceptions import ServiceException, NotFoundException
from app.schemas.student import StudentResponse, StudentCreateResponse, \
    StudentCreate, \
    StudentUpdate, StudentUpdateResponse
from app.services.user import ServiceUser
from app.utils.utils import send_new_account_email

router: APIRouter = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[StudentResponse])
async def get_users(
        current_user: CurrentUser,
        user_service: ServiceUser,
        skip: NonNegativeInt = Query(
            0, title='Skip', description='Skip users', example=0),
        limit: PositiveInt = Query(
            100, title='Limit', description='Limit pagination', example=100),
) -> list[StudentResponse]:
    """
    Get all Students basic information from the system using pagination.
    - `:param skip:` **Offset from where to start returning users**
    - `:type skip:` **NonNegativeInt**
    - `:param limit:` **Limit the number of results from query**
    - `:type limit:` **PositiveInt**
    - `:return:` **List of Students retrieved from database with id, username,
     email, first_name, last_name, is_active, is_superuser, created_at,
       updated_at.**
    - `:rtype:` **list[StudentResponse]**
    \f
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        found_users: list[StudentResponse] = await user_service.get_users(
            skip, limit)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(serv_exc)) from serv_exc
    return found_users


@router.post('', response_model=StudentCreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
        background_tasks: BackgroundTasks,
        user_service: ServiceUser,
        user: StudentCreate = Body(..., title='New user',
                                description='New user to register')
) -> StudentCreateResponse:
    """
    Register new user into the system.
    - `:param user:` **Body Object with username, email, first name,
     last name, password.**
    - `:type user:` **StudentCreate**
    - `:return:` **Student created with its id, username, email, first name
     and middle name.**
    - `:rtype:` **StudentCreateResponse**
    \f
    :param background_tasks: Send email to confirm registration
    :type background_tasks: BackgroundTasks
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    """
    try:
        new_user = await user_service.register_user(user)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Error at creating user.\n{str(serv_exc)}') from serv_exc
    if new_user:
        if user.email:
            background_tasks.add_task(
                send_new_account_email, user.email, user.username)
    return new_user


@router.get("/me", response_model=StudentResponse)
async def get_user_me(
        current_user: CurrentUser,
        user_service: ServiceUser,
) -> StudentResponse:
    """
    Get current user.
    - `:return:` **Response object for current user with id, username,
     email, first_name, last_name, is_active, is_superuser, created_at,
       updated_at.**
    - `:rtype:` **StudentResponse**
    \f
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    """
    try:
        user: StudentResponse = await user_service.get_user_by_id(
            current_user.id)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Can't not found user information.\n{str(serv_exc)}"
        ) from serv_exc
    return user


@router.get("/{user_id}", response_model=StudentResponse)
async def get_user_by_id(
        current_user: CurrentUser,
        user_service: ServiceUser,
        user_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1)
) -> StudentResponse:
    """
    Get an existing user from the system given an ID.
    - `:param user_id:` **Unique identifier of the user**
    - `:type user_id:` **PositiveInt**
    - `:return:` **Found user with the given ID including its username,
     email, first_name, last_name, is_active, is_superuser, created_at,
       updated_at.**
    - `:rtype:` **StudentResponse**
    \f
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        user: StudentResponse = await user_service.get_user_by_id(user_id)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {user_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc
    except NotFoundException as not_found_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc)) from not_found_exc
    return user


@router.put("/{user_id}", response_model=StudentUpdateResponse)
async def update_user(
        current_user: CurrentUser,
        user_service: ServiceUser,
        user_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1),
        user_in: StudentUpdate = Body(
            ..., title='Student data', description='New user data to update')
) -> StudentUpdateResponse:
    """
    Update an existing user from the system given an ID and new info.
    - `:param user_id:` **Unique identifier of the user**
    - `:type user_id:` **PositiveInt**
    - `:param user_in:` **New user data to update that can include:
     username, email, first_name, last_name, password.**
    - `:type user_in:` **StudentUpdate**
    - `:return:` **Updated user with the given ID and its username, email,
     first_name, last_name, hashed password, is_active, is_superuser,
       created_at and updated_at.**
    - `:rtype:` **StudentUpdateResponse**
    \f
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        user: StudentUpdateResponse = await user_service.update_user(
            user_id, user_in)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Student with id {user_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        current_user: CurrentUser,
        user_service: ServiceUser,
        user_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1)
) -> Response:
    """
    Delete an existing user from the system given an ID and new info.
    - `:param user_id:` **Unique identifier of the user**
    - `:type user_id:` **PositiveInt**
    - `:return:` **Json Response object with the deleted information**
    - `:rtype:` **Response**
    \f
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        data: dict = await user_service.delete_user(user_id)
    except SQLAlchemyError as sa_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The user with this username does not exist in the system"
                   f"\n{str(sa_err)}",
        ) from sa_err
    response: Response = Response(
        status_code=status.HTTP_204_NO_CONTENT,
        media_type='application/json')
    response.headers['deleted'] = str(data['ok']).lower()
    response.headers['deleted_at'] = str(data['deleted_at'])
    return response
