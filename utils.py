from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel

class Paginator(BaseModel):
    page: int
    per_page: int

def pagination_params(
        page: int = Query(ge=1, default=1, required=False, description="Page number"),
        per_page: int = Query(ge=1, lt=40, default=5, required=False, description="Records per page"),
):
    return Paginator.model_validate({"page": page, "per_page": per_page})


pagination_dep = Annotated[Paginator, Depends(pagination_params)]