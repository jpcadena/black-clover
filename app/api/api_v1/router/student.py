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
from app.schemas.grimoire import Grimoire
from app.schemas.student import StudentResponse, StudentCreateResponse, \
    StudentCreate, StudentUpdate
from app.services.student import ServiceStudent
from app.utils.utils import send_new_account_email

router: APIRouter = APIRouter(prefix="/students", tags=["students"])


@router.post('', response_model=StudentCreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create_student_request(
        background_tasks: BackgroundTasks,
        student_service: ServiceStudent,
        student_request: StudentCreate = Body(
            ..., title='New student', description='New student to register')
) -> StudentCreateResponse:
    """
    Register new student request into the system.
    - `:param student_request:` **Body Object with username, email, first name,
     last name, password, identification, magic affinity and age**
    - `:type student_request:` **StudentCreate**
    - `:return:` **Student request with its information.**
    - `:rtype:` **StudentCreateResponse**
    \f
    :param background_tasks: Send email to confirm registration
    :type background_tasks: BackgroundTasks
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    """
    try:
        new_student: StudentCreateResponse = await\
            student_service.create_student(student_request)
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


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_request(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        student_id: PositiveInt = Path(
            ..., title='Student ID',
            description='ID of the Student to searched', example=1),
        student_in: StudentUpdate = Body(
            ..., title='Student data',
            description='New student data to update')
) -> StudentResponse:
    """
    Update an existing student request from the system given an ID and
     new info.
    - `:param student_id:` **Unique identifier of the student**
    - `:type student_id:` **PositiveInt**
    - `:param student_in:` **New student data to update that can include:
     username, email, first_name, last_name, password.**
    - `:type student_in:` **StudentUpdate**
    - `:return:` **Updated student request with its information.**
    - `:rtype:` **StudentResponse**
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        student: StudentResponse = await student_service.update_student(
            student_id, student_in)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Student with id {student_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc
    return student


@router.patch("/{student_id}/status", response_model=StudentResponse)
async def update_student_status(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        student_id: PositiveInt = Path(
            ..., title='Student ID',
            description='ID of the Student to searched', example=1),
        request_status: bool = Path(
            ..., title='Student request status',
            description='Status of the student request', example=True)
) -> StudentResponse:
    """
    Update the status of the student request.
    - `:param student_id:` **Unique identifier of the student**
    - `:type student_id:` **PositiveInt**
    - `:param request_status:` **Status of the student request'**
    - `:type request_status:` **bool**
    - `:return:` **Updated student request with its information.**
    - `:rtype:` **StudentResponse**
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        student: StudentResponse = await student_service.update_student_status(
            student_id, request_status)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Student with id {student_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc
    return student


@router.get('', response_model=list[StudentResponse])
async def get_students_requests(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        skip: NonNegativeInt = Query(
            0, title='Skip', description='Skip students', example=0),
        limit: PositiveInt = Query(
            100, title='Limit', description='Limit pagination', example=100),
) -> list[StudentResponse]:
    """
    Get all students requests from the system using pagination.
    - `:param skip:` **Offset from where to start returning students**
    - `:type skip:` **NonNegativeInt**
    - `:param limit:` **Limit the number of results from query**
    - `:type limit:` **PositiveInt**
    - `:return:` **List of Students retrieved from database with its
    information.**
    - `:rtype:` **list[StudentResponse]**
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        found_students: list[StudentResponse] = await \
            student_service.get_students(skip, limit)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(serv_exc)) from serv_exc
    if not found_students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No students found in the system.')
    return found_students


@router.get("/{student_id}/grimoire", response_model=Grimoire)
async def get_student_grimoire_assignation(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        student_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1)
) -> Grimoire:
    """
    Get student grimoire assignment.
    - `:param student_id:` **Unique identifier of the student**
    - `:type student_id:` **PositiveInt**
    :return: Grimoire assigned to the student
    :rtype: Grimoire
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        grimoire: Grimoire = await student_service.get_grimoire_by_id(
            student_id)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc
    except NotFoundException as not_found_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc)) from not_found_exc
    return grimoire


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_request(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        student_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1)
) -> Response:
    """
    Delete an existing student request from the system given an ID and
     new info.
    - `:param student_id:` **Unique identifier of the student**
    - `:type student_id:` **PositiveInt**
    - `:return:` **Json Response object with the deleted information**
    - `:rtype:` **Response**
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        data: dict = await student_service.delete_student(student_id)
    except SQLAlchemyError as sa_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The student does not exist in the system"
                   f"\n{str(sa_err)}",
        ) from sa_err
    response: Response = Response(
        status_code=status.HTTP_204_NO_CONTENT,
        media_type='application/json')
    response.headers['deleted'] = str(data['ok']).lower()
    response.headers['deleted_at'] = str(data['deleted_at'])
    return response


@router.get("/me", response_model=StudentResponse)
async def get_my_request(
        current_user: CurrentUser,
        student_service: ServiceStudent,
) -> StudentResponse:
    """
    Get current student request.
    - `:return:` **Response object for current student with its
     information.**
    - `:rtype:` **StudentResponse**
    \f
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    """
    try:
        student: StudentResponse = await student_service.get_student_by_id(
            current_user.id)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Can't not found student information.\n{str(serv_exc)}"
        ) from serv_exc
    except NotFoundException as not_found_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc)) from not_found_exc
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_request_by_id(
        current_user: CurrentUser,
        student_service: ServiceStudent,
        student_id: PositiveInt = Path(
            ..., title='Student ID', description='ID of the Student to '
                                                 'searched',
            example=1)
) -> StudentResponse:
    """
    Get an existing student request from the system given an ID.
    - `:param student_id:` **Unique identifier of the student**
    - `:type student_id:` **PositiveInt**
    - `:return:` **Found student with the given information.**
    - `:rtype:` **StudentResponse**
    \f
    :param student_service: Dependency method for student service layer
    :type student_service: ServiceStudent
    :param current_user: Dependency method for authorization by current user
    :type current_user: CurrentStudent
    """
    try:
        student: StudentResponse = await student_service.get_student_by_id(
            student_id)
    except ServiceException as serv_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found in the system."
                   f"\n{str(serv_exc)}") from serv_exc
    except NotFoundException as not_found_exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(not_found_exc)) from not_found_exc
    return student
