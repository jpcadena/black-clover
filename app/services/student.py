"""
Student Service to handle business logic
"""
from datetime import datetime
from typing import Optional, Type, Annotated, List
from fastapi import Depends
from pydantic import PositiveInt, NonNegativeInt
from app.core.security.exceptions import DatabaseException, ServiceException, \
    NotFoundException
from app.crud.specification import IdSpecification
from app.crud.student import StudentRepository, get_student_repository
from app.models.student import Student
from app.schemas.student import StudentResponse, StudentCreate, StudentUpdate
from app.services import model_to_response


class StudentService:
    """
    Student service class
    """

    def __init__(self, student_repo: StudentRepository):
        self.student_repo: StudentRepository = student_repo

    async def get_student_by_id(
            self, student_id: PositiveInt) -> Optional[StudentResponse]:
        """
        Retrieve student information with the correct schema for response
        :param student_id: Unique identifier of the student
        :type student_id: PositiveInt
        :return: Student information
        :rtype: StudentResponse
        """
        try:
            student: Student = await self.student_repo.read_by_id(
                IdSpecification(student_id))
        except DatabaseException as db_exc:
            raise ServiceException(str(db_exc)) from db_exc
        if not student:
            raise NotFoundException(
                f"Student with id {student_id} not found in the system.")
        student_response: Optional[StudentResponse] = await model_to_response(
            student, StudentResponse)
        return student_response

    async def get_all_students(
            self, offset: NonNegativeInt, limit: PositiveInt
    ) -> List[StudentResponse]:
        """
        Retrieve all students in the system.
        :param offset: Offset from where to start returning students
        :type offset: NonNegativeInt
        :param limit: Limit the number of results from query
        :type limit: PositiveInt
        :return: A list of students
        :rtype: List[StudentResponse]
        """
        try:
            students: list[Student] = await self.student_repo.read_students(
                offset, limit)
        except DatabaseException as db_exc:
            raise ServiceException(str(db_exc)) from db_exc
        found_students: list[Optional[StudentResponse]] = [
            await model_to_response(student, StudentResponse) for student in
            students]
        return found_students

    async def create_student(
            self, student: StudentCreate) -> Optional[StudentResponse]:
        """
        Create a new student in the database.
        :param student: Request object representing the student
        :type student: StudentCreate
        :return: Response object representing the created student in the
                 database
        :rtype: StudentResponse
        """
        try:
            created_student = await self.student_repo.create_student(student)
        except DatabaseException as db_exc:
            raise ServiceException(str(db_exc)) from db_exc
        return await model_to_response(created_student, StudentResponse)

    async def update_student(
            self, student_id: PositiveInt, student: StudentUpdate
    ) -> Optional[StudentResponse]:
        """
        Update student information in the database.
        :param student_id: Unique identifier of the student
        :type student_id: PositiveInt
        :param student: Requested student information to update
        :type student: StudentUpdate
        :return: Updated student information
        :rtype: StudentResponse
        """
        try:
            updated_student: Student = await self.student_repo.update_student(
                IdSpecification(student_id), student)
        except DatabaseException as db_exc:
            raise ServiceException(str(db_exc)) from db_exc
        return await model_to_response(updated_student, StudentResponse)

    async def delete_student(self, student_id: PositiveInt) -> dict:
        """
        Delete a student from the database.
        :param student_id: Unique identifier of the student
        :type student_id: PositiveInt
        :return: Data to confirmation info about the delete process
        :rtype: dict
        """
        try:
            deleted: bool = await self.student_repo.delete_student(
                IdSpecification(student_id))
        except DatabaseException as db_exc:
            raise ServiceException(str(db_exc)) from db_exc
        return {"ok": deleted, 'deleted_at': datetime.now()}


async def get_student_service(
        student_repo: StudentRepository = Depends(
            get_student_repository)) -> StudentService:
    """
    Get an instance of the student service with the given repository.
    :param student_repo: Student repository object for database connection
    :type student_repo: StudentRepository
    :return: StudentService instance with repository associated
    :rtype: StudentService
    """
    return StudentService(student_repo)


ServiceUser: Type[StudentService] = Annotated[
    StudentService, Depends(get_student_service)]
