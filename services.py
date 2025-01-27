import functools
from typing import TypeVar, Iterable, Callable
from sqlalchemy.orm import Session

from repositories.tasks import TasksRepository
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema, ReadTaskSchema
from utils import Paginator

Repository = TypeVar("Repository")

def inject_session(repository: type[Repository], session: Session) -> Repository:
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
    def __init__(self, repositories: Iterable[type[Repository]], session: type[Session]):
        self._repositories = repositories
        self.prepared_repositories = Registry()
        self.session = session
        self.__prepare_repositories_with_session()

    def __prepare_repositories_with_session(self) -> Session:
        session = self.session()
        for repo in self._repositories:
            self.prepared_repositories.register(repo, inject_session(repo, session))
        return session


    def create_task(self, new_task: CreateTaskSchema):
        session = self.__prepare_repositories_with_session()
        with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            tasks_repo.create_new_task(new_task)
            session.commit()

    def delete_task(self, task_name: str):
        session = self.__prepare_repositories_with_session()
        with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            tasks_repo.delete_task(task_name)
            session.commit()

    def update_task(self, task_name: str, updated_task: UpdateTaskSchema):
        session = self.__prepare_repositories_with_session()
        with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            tasks_repo.update_task(task_name, updated_task)
            session.commit()

    def get_tasks(self, paginator: Paginator) -> list[ReadTaskSchema]:
        session = self.__prepare_repositories_with_session()
        with session as session:
            tasks_repo = self.prepared_repositories.get(TasksRepository)
            tasks = tasks_repo.get_tasks(paginator)
            session.commit()
        return tasks