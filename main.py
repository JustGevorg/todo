from fastapi import FastAPI

from api.tasks import tasks_api_router
from exceptions.exception_handlers import add_exception_handlers, EXCEPTION_HANDLERS

app = FastAPI(title="TODO list api", description="API управления заметками")
app.include_router(tasks_api_router)
app = add_exception_handlers(app, EXCEPTION_HANDLERS)
