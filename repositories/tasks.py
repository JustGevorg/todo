import sqlalchemy
from sqlalchemy import insert, delete, update, select
from exceptions.exceptions import TaskAlreadyExists, TaskNotExistsException
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema, ReadTaskSchema
from repositories.base import SqlalchemyRepository
from database.models import Task
from utils import Paginator


class TasksRepository(SqlalchemyRepository):

    def create_new_task(self, new_task: CreateTaskSchema) -> None:
        stmt = insert(Task).values(new_task.model_dump())
        try:
            self.session.execute(stmt)
        except sqlalchemy.exc.IntegrityError:
            raise TaskAlreadyExists(description=f"Задача с названием '{new_task.name}' уже существует!")

    def delete_task(self, task_name: str) -> None:
        stmt = delete(Task).where(Task.name == task_name).returning(Task.name)
        affected_task_name= self.session.execute(stmt).scalars().first()
        if not affected_task_name:
            raise TaskNotExistsException(f"Удаляемой задачи с именем '{task_name}' не существует!")

    def update_task(self, task_name: str, new_task: UpdateTaskSchema) -> None:
        stmt = update(Task).values(new_task.model_dump()).where(Task.name == task_name).returning(Task.name)
        updated_task_name = self.session.execute(stmt).scalars().first()
        if not updated_task_name:
            raise TaskNotExistsException(f"Обновляемой задачи с именем '{task_name}' не существует!")


    def get_tasks(self, pagination: Paginator | None = None) -> list[ReadTaskSchema]:
        query = select(Task).limit(pagination.per_page).offset((pagination.page - 1) * pagination.per_page)
        get_tasks_query_result = self.session.execute(query).all()
        tasks = [ReadTaskSchema.model_validate(task[0], from_attributes=True) for task in get_tasks_query_result]
        if len(tasks) == 0:
            raise TaskNotExistsException(f"Задач не найдено!")

        return tasks
