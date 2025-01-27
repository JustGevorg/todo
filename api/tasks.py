import asyncio
from typing import Annotated

from fastapi import APIRouter, Path, Depends

from api.responses import create_new_task_responses
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema
from use_cases import UseCases
from utils import pagination_dep, Stub

tasks_api_router = APIRouter(prefix="/tasks", tags=["tasks"])

# TODO: добавить примеры ответов для каждого эндпоинта
@tasks_api_router.post("",
                       description="Create a new task",
                       summary="Create a new task",
                       responses=create_new_task_responses)
async def create_new_task(use_cases: Annotated[UseCases, Depends(Stub(UseCases))],
                    new_task: CreateTaskSchema):
    await use_cases.create_task(new_task)


@tasks_api_router.delete("/{task_name}",
                         description="Delete a task",
                         summary="Delete a task")
async def delete_task(use_cases: Annotated[UseCases, Depends(Stub(UseCases))],
                task_name: str = Path(description="Task name")):
    await use_cases.delete_task(task_name)


@tasks_api_router.put("/{task_name}",
                      description="Update a task",
                      summary="Update a task")
async def update_task(use_cases: Annotated[UseCases, Depends(Stub(UseCases))],
                updated_task: UpdateTaskSchema, task_name: str = Path(description="Task name")):
    await use_cases.update_task(task_name, updated_task)


@tasks_api_router.get("",
                      description="Get all tasks",
                      summary="Get all tasks")
async def get_tasks(use_cases: Annotated[UseCases, Depends(Stub(UseCases))],
                    pagination: pagination_dep):
    tasks = await use_cases.get_tasks(pagination)
    return tasks
