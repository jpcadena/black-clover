"""
Filter script
"""
import logging
from abc import ABC, abstractmethod
from typing import Optional, Union
from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.decorators import with_logging, benchmark
from app.crud.specification import Specification, IdSpecification, \
    UsernameSpecification, EmailSpecification
from app.models.student import Student
from app.models.user import User
from app.schemas.grimoire import Grimoire

logger: logging.Logger = logging.getLogger(__name__)


class Filter(ABC):
    """
    Filter class
    """

    @abstractmethod
    async def filter(
            self, spec: Specification, session: AsyncSession,
            model: Union[User, Student], field: str
    ) -> Optional[Union[User, Student]]:
        """
        Filter method
        :param spec: specification to filter by
        :type spec: Specification
        :param session: Async Session for Database
        :type session: AsyncSession
        :param model: Datatable model
        :type model: User or Student
        :param field: The field for UniqueFilter
        :type field: str
        :return: Datatable model instance
        :rtype: User or Student
        """


class IndexFilter(Filter):
    """
    User Filter class based on Filter for ID.
    """

    @with_logging
    @benchmark
    async def filter(
            self, spec: IdSpecification, session: AsyncSession,
            model: Union[User, Student, Grimoire], field: str = None
    ) -> Optional[Union[User, Student, Grimoire]]:
        async with session as async_session:
            if field:
                try:
                    stmt: Select = select(model).where(
                        model.id == spec.value)
                    db_obj = await async_session.scalar(stmt)
                except SQLAlchemyError as sa_exc:
                    logger.error(sa_exc)
                    raise sa_exc
            else:
                try:
                    db_obj = await async_session.get(model, spec.value)
                except SQLAlchemyError as sa_exc:
                    logger.error(sa_exc)
                    raise sa_exc
            logger.info('Retrieving row with id: %s', spec.value)
            return db_obj


class UniqueFilter(Filter):
    """
    Unique Filter class based on Filter for Username and Email.
    """

    @with_logging
    @benchmark
    async def filter(
            self, spec: Union[UsernameSpecification, EmailSpecification],
            session: AsyncSession, model: User, field: str = "email"
    ) -> Union[User]:
        if field == "username":
            stmt: Select = select(model).where(model.username == spec.value)
        elif field == "email":
            stmt: Select = select(model).where(model.email == spec.value)
        else:
            raise ValueError("Invalid field specified for filtering")
        async with session as async_session:
            try:
                db_obj = (await async_session.scalars(stmt)).one()
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                raise sa_exc
            logger.info('Retrieving row with filter: %s', spec.value)
            return db_obj


async def get_index_filter() -> IndexFilter:
    """
    Get an IndexFilter instance
    :return: IndexFilter instance
    :rtype: IndexFilter
    """
    return IndexFilter()


async def get_unique_filter() -> UniqueFilter:
    """
    Get an UniqueFilter instance
    :return: UniqueFilter instance
    :rtype: UniqueFilter
    """
    return UniqueFilter()
