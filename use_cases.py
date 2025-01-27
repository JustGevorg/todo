import asyncio
import functools
from typing import TypeVar, Iterable, Callable
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.tasks import TasksRepository
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema, ReadTaskSchema
from utils import Paginator

Repository = TypeVar("Repository")

def inject_session(repository: type[Repository], session: Session | AsyncSession) -> Repository:
    return repository(session)

T = TypeVar('T')

class Registry:
    def __init__(self):
        self._registry: dict[type[T], T] = {}

    def register(self, cls: type[T], instance: T) -> None:
        self._registry[cls] = instance

    def get(self, cls: type[T]) -> T | None:
        return self._registry.get(cls)


class UseCases:
    def __init__(self, repositories: Iterable[type[Repository]], session: type[Session] | type[AsyncSession]):
        self._repositories = repositories
        self.prepared_repositories = Registry()
        self.session = session
        self.__prepare_repositories_with_session()

    def __prepare_repositories_with_session(self) -> Session | AsyncSession:
        session = self.session()
        for repo in self._repositories:
            self.prepared_repositories.register(repo, inject_session(repo, session))
        return session


    async def create_task(self, new_task: CreateTaskSchema):
        session = self.__prepare_repositories_with_session()
        async with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            await tasks_repo.create_new_task(new_task)
            await session.commit()

    async def delete_task(self, task_name: str):
        session = self.__prepare_repositories_with_session()
        async with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            await tasks_repo.delete_task(task_name)
            await session.commit()

    async def update_task(self, task_name: str, updated_task: UpdateTaskSchema):
        session = self.__prepare_repositories_with_session()
        async with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            await tasks_repo.update_task(task_name, updated_task)
            await session.commit()

    async def get_tasks(self, paginator: Paginator) -> list[ReadTaskSchema]:
        session = self.__prepare_repositories_with_session()
        async with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            tasks = await tasks_repo.get_tasks(paginator)
            await session.commit()
        return tasks