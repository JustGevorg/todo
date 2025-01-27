from typing import Annotated

from fastapi import APIRouter, Path, Depends
from repositories.tasks import TasksRepository
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema
from services import UseCases
from utils import pagination_dep, Stub

tasks_api_router = APIRouter(prefix="/tasks", tags=["tasks"])

# TODO: добавить примеры ответов для каждого эндпоинта

# @tasks_api_router.post("",
#                        description="Create a new task",
#                        summary="Create a new task")
# def create_new_task(tasks_repo: Annotated[TasksRepository, Depends(Stub(TasksRepository))],
#                     new_task: CreateTaskSchema):
#     with tasks_repo.session as session:
#         tasks_repo.create_new_task(new_task)
#         session.commit()

@tasks_api_router.post("",
                       description="Create a new task",
                       summary="Create a new task")
def create_new_task(use_cases: Annotated[UseCases, Depends(Stub(UseCases))],
                    new_task: CreateTaskSchema):
    use_cases.create_task(new_task)


@tasks_api_router.delete("/{task_name}",
                         description="Delete a task",
                         summary="Delete a task")
def delete_task(tasks_repo: Annotated[TasksRepository, Depends(Stub(TasksRepository))],
                task_name: str = Path(description="Task name")):
    with tasks_repo.session as session:
        tasks_repo.delete_task(task_name)
        session.commit()


@tasks_api_router.put("/{task_name}",
                      description="Update a task",
                      summary="Update a task")
def update_task(tasks_repo: Annotated[TasksRepository, Depends(Stub(TasksRepository))],
                updated_task: UpdateTaskSchema, task_name: str = Path(description="Task name")):
    with tasks_repo.session as session:
        tasks_repo.update_task(task_name, updated_task)
        session.commit()


@tasks_api_router.get("",
                      description="Get all tasks",
                      summary="Get all tasks")
async def get_tasks(tasks_repo: Annotated[TasksRepository, Depends(Stub(TasksRepository))],
                    pagination: pagination_dep):
    with tasks_repo.session as session:
        tasks = tasks_repo.get_tasks(pagination)
        session.commit()

    return tasks
