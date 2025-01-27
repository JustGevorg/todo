import asyncio

import sqlalchemy
from sqlalchemy import insert, delete, update, select
from exceptions.exceptions import TaskAlreadyExists, TaskNotExistsException
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema, ReadTaskSchema
from repositories.base import SqlalchemyRepository
from database.models import Task
from utils import Paginator
from resources import ExceptionsDescriptionsTemplates


class TasksRepository(SqlalchemyRepository):

    async def create_new_task(self, new_task: CreateTaskSchema) -> None:
        stmt = insert(Task).values(new_task.model_dump())
        try:
            await self.session.execute(stmt)
        except sqlalchemy.exc.IntegrityError:
            raise TaskAlreadyExists(
                description=ExceptionsDescriptionsTemplates.task_with_name_already_exists.format(task_name=new_task.name))

    async def delete_task(self, task_name: str) -> None:
        stmt = delete(Task).where(Task.name == task_name).returning(Task.name)
        affected_task_name = await self.session.scalars(stmt)
        if not affected_task_name.first():
            raise TaskNotExistsException(
                ExceptionsDescriptionsTemplates.deleted_task_not_exists.format(task_name=task_name))

    async def update_task(self, task_name: str, new_task: UpdateTaskSchema) -> None:
        stmt = update(Task).values(new_task.model_dump()).where(Task.name == task_name).returning(Task.name)
        updated_task_name = await self.session.scalars(stmt)

        updated_task_name = updated_task_name.first()
        if not updated_task_name:
            raise TaskNotExistsException(
                ExceptionsDescriptionsTemplates.updated_task_not_exists.format(task_name=task_name))

    async def get_tasks(self, pagination: Paginator | None = None) -> list[ReadTaskSchema]:
        query = select(Task).limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page)
        get_tasks_query_result = await self.session.scalars(query)
        tasks = [ReadTaskSchema.model_validate(task, from_attributes=True) for task in get_tasks_query_result]
        if len(tasks) == 0:
            raise TaskNotExistsException(ExceptionsDescriptionsTemplates.tasks_not_found)

        return tasks
