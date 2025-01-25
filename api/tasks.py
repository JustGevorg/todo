from fastapi import APIRouter, Path
from repositories.tasks import TasksRepository
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema
from database.database_config import sync_session_maker
from utils import pagination_dep

tasks_api_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_api_router.post("",
                       description="Create a new task",
                       summary="Create a new task")
def create_new_task(new_task: CreateTaskSchema):
    repo = TasksRepository(session=sync_session_maker())
    repo.create_new_task(new_task)
    repo.session.commit()
    repo.session.close()

@tasks_api_router.delete("/{task_name}",
                         description="Delete a task",
                         summary="Delete a task")
def remove_task(task_name: str = Path(description="Task name")):
    repo = TasksRepository(session=sync_session_maker())
    repo.remove_task(task_name)
    repo.session.commit()
    repo.session.close()


@tasks_api_router.put("/{task_name}",
                      description="Update a task",
                      summary="Update a task")
def update_task(updated_task: UpdateTaskSchema, task_name: str = Path(description="Task name")):
    repo = TasksRepository(session=sync_session_maker())
    repo.update_task(task_name, updated_task)
    repo.session.commit()
    repo.session.close()

@tasks_api_router.get("",
                      description="Get all tasks",
                      summary="Get all tasks")
def get_tasks(pagination: pagination_dep):
    repo = TasksRepository(session=sync_session_maker())
    tasks = repo.get_tasks(pagination)
    repo.session.commit()
    repo.session.close()
    return tasks
