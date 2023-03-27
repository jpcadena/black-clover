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
    StudentCreate, StudentUpdate
from app.services.user import ServiceUser
from app.utils.utils import send_new_account_email

router: APIRouter = APIRouter(prefix="/students", tags=["students"])


@router.post('', response_model=StudentCreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
        background_tasks: BackgroundTasks,
        student_service: ServiceUser,
        student_request: StudentCreate = Body(..., title='New student',
                                description='New student to register')
) -> StudentCreateResponse:
    """
    Register new student into the system.
    - `:param student_request:` **Body Object with username, email, first name,
     last name, password.**
    - `:type student_request:` **StudentCreate**
    - `:return:` **Student created with its id, username, email, first name
     and middle name.**
    - `:rtype:` **StudentCreateResponse**
    \f
    :param background_tasks: Send email to confirm registration
    :type background_tasks: BackgroundTasks
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    """
    try:
        new_student = await student_service.register_student(student_request)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'Error at creating student.\n{str(serv_exc)}') from \
            serv_exc
    if new_student:
        if student_request.user.email:
            background_tasks.add_task(
                send_new_account_email, student_request.user.email,
                student_request.user.username)
    return new_student


# @router.post("/", response_model=schemas.StudentResponse)
# async def create_student(
#     *,
#     db: Session = Depends(deps.get_db),
#     student_in: schemas.StudentCreate
# ) -> schemas.StudentResponse:
#     """
#     Enviar solicitud de ingreso.
#     """
#     user = crud.user.create(db, obj_in=student_in.user)
#     student = crud.student.create_with_user(db, obj_in=student_in, user_id=user.id)
#     return student


@router.get("", response_model=list[StudentResponse])
async def get_students(
        current_user: CurrentUser,
        user_service: ServiceUser,
        skip: NonNegativeInt = Query(
            0, title='Skip', description='Skip students', example=0),
        limit: PositiveInt = Query(
            100, title='Limit', description='Limit pagination', example=100),
) -> list[StudentResponse]:
    """
    Get all Students basic information from the system using pagination.
    - `:param skip:` **Offset from where to start returning students**
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
        found_students: list[StudentResponse] = await \
            user_service.get_students(
            skip, limit)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(serv_exc)) from serv_exc
    return found_students


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


@router.put("/{user_id}", response_model=StudentResponse)
async def update_user(
        current_user: CurrentUser,
        user_service: ServiceUser,
        user_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1),
        user_in: StudentUpdate = Body(
            ..., title='Student data', description='New user data to update')
) -> StudentResponse:
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
    - `:rtype:` **StudentResponse**
    \f
    :param user_service: Dependency method for user service layer
    :type user_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        user: StudentResponse = await user_service.update_user(
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


# @router.put("/{student_id}", response_model=schemas.StudentResponse)
# async def update_student(
#     *,
#     db: Session = Depends(deps.get_db),
#     student_id: int,
#     student_in: schemas.StudentUpdate
# ) -> schemas.StudentResponse:
#     """
#     Actualizar solicitud de ingreso.
#     """
#     student = crud.student.get(db, id=student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#
#     student = crud.student.update(db, db_obj=student, obj_in=student_in)
#     return student
#
#
# @router.patch("/{student_id}/status", response_model=schemas.StudentResponse)
# async def update_student_status(
#     *,
#     db: Session = Depends(deps.get_db),
#     student_id: int,
#     status: bool
# ) -> schemas.StudentResponse:
#     """
#     Actualizar estatus de solicitud.
#     """
#     student = crud.student.get(db, id=student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#
#     student = crud.student.update_status(db, db_obj=student, status=status)
#     return student
#
#
# @router.get("/", response_model=List[schemas.StudentResponse])
# async def read_students(
#     *,
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100
# ) -> List[schemas.StudentResponse]:
#     """
#     Consultar todas las solicitudes.
#     """
#     students = crud.student.get_multi(db, skip=skip, limit=limit)
#     return students
#
#
# @router.get("/{student_id}/grimoire", response_model=schemas.GrimoireAssignment)
# async def read_student_grimoire(
#     *,
#     db: Session = Depends(deps.get_db),
#     student_id: int
# ) -> schemas.GrimoireAssignment:
#     """
#     Consultar asignaciones de Grimorios.
#     """
#     student = crud.student.get(db, id=student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#
#     grimoire_assignment = crud.student.get_grimoire_assignment(db, student=student)
#     return grimoire_assignment
#
#
# @router.delete("/{student_id}", response_model=schemas.StudentResponse)
# async def delete_student(
#     *,
#     db: Session = Depends(deps.get_db),
#     student_id: int
# ) -> schemas.StudentResponse:
#     """
#     Eliminar solicitud de ingreso.
#     """
#     student = crud.student.get(db, id=student_id)
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#
#     student = crud.student.remove(db, id=student_id)
#     return student
