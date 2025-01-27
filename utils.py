from typing import Annotated, TypeVar, Callable, Any

from fastapi import Query, Depends
from pydantic import BaseModel


class Paginator(BaseModel):
    page: int
    per_page: int

def pagination_params(
        page: int = Query(ge=1, default=1, required=False, description="Page number"),
        per_page: int = Query(ge=1, lt=40, default=5, required=False, description="Records per page"),
) -> Paginator:
    return Paginator.model_validate({"page": page, "per_page": per_page})


pagination_dep = Annotated[Paginator, Depends(pagination_params)]

class Stub:
    def __init__(self, dependency: Callable[..., Any]) -> None:
        """Сохраняем нашу абстракцию."""
        self._dependency = dependency

    def __call__(self) -> None:
        """Выкинем ошибку, если забыли подменить реализацию при старте приложения."""
        raise NotImplementedError(f"You forgot to register `{self._dependency}` implementation.")

    def __hash__(self) -> int:
        """Обманываем app.dependency_overrides, чтобы он считал Stub реальной зависимостью"""
        return hash(self._dependency)

    def __eq__(self, __value: object) -> bool:
        """Обманываем app.dependency_overrides, чтобы он считал Stub реальной зависимостью"""
        if isinstance(__value, Stub):
            return self._dependency == __value._dependency
        else:
            return self._dependency == __value
