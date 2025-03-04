from typing import Any, Dict, Generic, List, Sequence, Type, TypeVar

import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from .base import Base


Model = TypeVar('Model', bound=Base)


class SqlAlchemyRepository(Generic[Model]):

    query_cls: Type[Query]

    def __init__(self, session: AsyncSession, model_cls: Model):
        self.session = session
        self.model_cls = model_cls

    def query(self, *entities) -> Query:
        return self.query_cls(entities, self.session)

    def create(self, **attrs) -> Model:
        return self.model_cls(**attrs)

    def merge(self, instance: Model, **attrs) -> Model:
        for attr_key, attr_value in attrs.items():
            setattr(instance, attr_key, attr_value)

        return instance

    def has_pk(self, instance: Model) -> bool:
        return bool(self.get_pk(instance))

    def get_pk(self, instance: Model) -> Dict[str, Any] | Any:
        server_default_pks = (
            pk
            for pk in self.model_cls.__mapper__.primary_key
            if pk.server_default is not None
        )
        pks = {
            pk.name: attr
            for pk in server_default_pks
            if (attr := getattr(instance, pk.name)) is not None
        }

        if len(pks) == 1:
            return next(iter(pks.values()))
        elif len(pks) > 1:
            return pks

    async def count(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> int:
        statement = sa.select(sa.func.count(
        )).select_from(self.model_cls).where(*where).filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def avg(
            self,
            *where,
            column,
            params: Any = None,
            bind_arguments: Any = None,
            **attrs,
    ) -> float:
        statement = sa.select(sa.func.avg(column).label('average'))\
            .select_from(self.model_cls).where(*where).filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def update(
        self,
        *where,
        values: Dict[str, Any],
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        statement = sa.update(
            self.model_cls,
        ).where(*where).filter_by(**attrs).values(**values)
        await self.session.execute(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )
        await self.session.commit()

    async def delete(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> None:
        statement = sa.delete(self.model_cls).where(*where).filter_by(**attrs)
        await self.session.execute(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )
        await self.session.commit()

    async def find(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> List[Model]:
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_with_group_by(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        group_by_item,
        ** attrs,
    ) -> List[Model]:
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs) \
            .group_by(group_by_item)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_with_order(self,
                              *where,
                              params: Any = None,
                              bind_arguments: Any = None,
                              order_item,
                              **attrs,
                              ):
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs) \
            .order_by(order_item)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_with_options(self,
                                *where,
                                params: Any = None,
                                bind_arguments: Any = None,
                                options: Any = None,
                                **attrs,
                                ) -> List[Model]:
        statement = sa.select(self.model_cls).where(*where)
        for option in options:
            statement = statement.options(option)
        statement = statement.filter_by(**attrs)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_distinct_with_options(self,
                                         *where,
                                         params: Any = None,
                                         bind_arguments: Any = None,
                                         options: Any = None,
                                         distinct_column,
                                         **attrs) -> List[Model]:
        sa.distinct
        statement = sa.select(self.model_cls).where(
            *where).distinct(distinct_column)
        for option in options:
            statement = statement.options(option)
        statement = statement.filter_by(**attrs)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_with_order_and_options(self,
                                          *where,
                                          params: Any = None,
                                          bind_arguments: Any = None,
                                          options: Any = None,
                                          order_item,
                                          **attrs,) -> List[Model]:
        statement = sa.select(self.model_cls).where(*where)
        for option in options:
            statement = statement.options(option)
        statement = statement.filter_by(**attrs).order_by(order_item)
        return (await self.session.scalars(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )).unique().all()

    async def find_one(
        self,
        *where,
        params: Any = None,
        bind_arguments: Any = None,
        **attrs,
    ) -> Model | None:
        statement = sa.select(self.model_cls).where(*where).filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def find_one_with_options(
            self,
            *where,
            params: Any = None,
            bind_arguments: Any = None,
            options: Any = None,
            **attrs,
    ) -> Model | None:
        statement = sa.select(self.model_cls).where(*where)
        if options and len(options) > 0:
            for option in options:
                statement = statement.options(option)
        statement = statement.filter_by(**attrs)
        return await self.session.scalar(
            statement=statement, params=params, bind_arguments=bind_arguments,
        )

    async def find_one_or_fail(self, *where, **attrs) -> Model:
        instance = await self.find_one(*where, **attrs)
        if instance is None:
            raise NoResultFound(
                '{0.__name__} not found'.format(self.model_cls))

        return instance

    async def remove(self, instance: Model) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def remove_many(self, instances: Sequence[Model]) -> None:
        for instance in instances:
            await self.session.delete(instance)

        await self.session.commit()

    async def pre_save(self, instance: Model, **kwargs) -> Model:
        if self.has_pk(instance):
            return await self.session.merge(instance, **kwargs)

        self.session.add(instance, **kwargs)
        await self.session.flush([instance])
        return instance

    async def pre_save_many(self, instances: Sequence[Model]) -> Sequence[Model]:
        self.session.add_all(instances)
        await self.session.flush(instances)
        return instances

    async def save(self, instance: Model, **kwargs) -> Model:
        instance = await self.pre_save(instance, **kwargs)
        await self.session.commit()
        return instance

    async def save_many(self, instances: Sequence[Model]) -> Sequence[Model]:
        instances = await self.pre_save_many(instances)
        await self.session.commit()
        return instances
