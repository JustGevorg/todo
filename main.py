from fastapi import FastAPI

from api.tasks import tasks_api_router
from exceptions.exception_handlers import add_exception_handlers, EXCEPTION_HANDLERS
from repositories.tasks import TasksRepository
from database.database_config import SyncSession, async_session
from use_cases import UseCases

app = FastAPI(title="TODO list api", description="API управления заметками")
def setup_dependedencies(app: FastAPI) -> FastAPI:

    use_cases = UseCases([TasksRepository], async_session)
    app.dependency_overrides.update({
        UseCases: lambda: use_cases,
    })

    return app

app.include_router(tasks_api_router)
app = setup_dependedencies(app)
app = add_exception_handlers(app, EXCEPTION_HANDLERS)
