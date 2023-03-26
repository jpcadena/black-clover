"""
Student CRUD script
"""
import logging
from datetime import datetime
from typing import Optional
from fastapi.encoders import jsonable_encoder
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.decorators import with_logging, benchmark
from app.core.security.exceptions import DatabaseException
from app.core.security.password import get_password_hash
from app.crud.filter import IndexFilter, UniqueFilter, get_index_filter, \
    get_unique_filter
from app.crud.specification import IdSpecification
from app.db.session import get_session
from app.models.student import Student
from app.schemas.student import StudentResponse

logger: logging.Logger = logging.getLogger(__name__)


class StudentRepository:
    """
    Repository class for Student.
    """

    def __init__(self, session: AsyncSession, index_filter: IndexFilter,
                 unique_filter: UniqueFilter):
        self.session: AsyncSession = session
        self.index_filter: IndexFilter = index_filter
        self.unique_filter: UniqueFilter = unique_filter
        self.model: Student = Student

    async def read_by_id(self, _id: IdSpecification) -> Optional[Student]:
        """
        Reads the student by its id
        :param _id:
        :type _id: IdSpecification
        :return: Student instance
        :rtype: Student
        """
        async with self.session as session:
            try:
                student: Student = await self.index_filter.filter(
                    _id, session, self.model)
            except SQLAlchemyError as db_exc:
                raise DatabaseException(str(db_exc)) from db_exc
            return student

    @with_logging
    @benchmark
    async def read_students(
            self, offset: NonNegativeInt, limit: PositiveInt,
    ) -> list[Student]:
        """
        Read students information from table
        :param offset: Offset from where to start returning students
        :type offset: NonNegativeInt
        :param limit: Limit the number of results from query
        :type limit: PositiveInt
        :return: Student information
        :rtype: Student
        """
        stmt: Select = select(Student).offset(offset).limit(limit)
        async with self.session as session:
            try:
                results: ScalarResult = await session.scalars(stmt)
                students: list[Student] = results.all()
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                raise DatabaseException(str(sa_exc)) from sa_exc
            return students

    @with_logging
    @benchmark
    async def create_student(
            self, student: StudentResponse,
    ) -> Student:
        """
        Create student into the database
        :param student: Request object representing the student
        :type student: StudentResponse
        :return: Response object representing the created student in the
         database
        :rtype: Student
        """
        async with self.session as session:
            try:
                session.add(student)
                await session.commit()
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                raise DatabaseException(str(sa_exc)) from sa_exc
            try:
                created_student: Student = await self.read_by_id(
                    IdSpecification(student.id))
            except DatabaseException as db_exc:
                raise DatabaseException(str(db_exc)) from db_exc
            return created_student

    @with_logging
    @benchmark
    async def update_student(
            self, student_id: IdSpecification, student: StudentResponse
    ) -> Optional[Student]:
        """
        Update student information from table
        :param student_id: Unique identifier of the student
        :type student_id: IdSpecification
        :param student: Requested student information to update
        :type student: StudentUpdate
        :return: Student information
        :rtype: Student
        """
        async with self.session as session:
            try:
                found_student: Student = await self.read_by_id(student_id)
            except DatabaseException as db_exc:
                raise DatabaseException(str(db_exc)) from db_exc
            obj_data: dict = jsonable_encoder(found_student)
            update_data: dict = student.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    if field == 'password':
                        setattr(found_student, field, await get_password_hash(
                            update_data[field]))
                    else:
                        setattr(found_student, field, update_data[field])
                if field == 'updated_at':
                    setattr(found_student, field, datetime.utcnow())
            session.add(found_student)
            await session.commit()
            try:
                updated_student: Student = await self.read_by_id(student_id)
            except DatabaseException as db_exc:
                raise DatabaseException(str(db_exc)) from db_exc
            return updated_student

    @with_logging
    @benchmark
    async def delete_student(self, student_id: IdSpecification) -> bool:
        """
        Deletes a student by its id
        :param student_id: Unique identifier of the student
        :type student_id: IdSpecification
        :return: True if the student is deleted; otherwise False
        :rtype: bool
        """
        async with self.session as session:
            try:
                found_student: Student = await self.read_by_id(student_id)
            except DatabaseException as db_exc:
                raise DatabaseException(str(db_exc)) from db_exc
            try:
                await session.delete(found_student)
                await session.commit()
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                await session.rollback()
                raise DatabaseException(str(sa_exc)) from sa_exc
            return True


async def get_student_repository() -> StudentRepository:
    """
    Get an instance of the student repository with the given session.
    :return: StudentRepository instance with session associated
    :rtype: StudentRepository
    """
    return StudentRepository(
        await get_session(), await get_index_filter(),
        await get_unique_filter())
