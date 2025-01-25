from pydantic import BaseModel, constr


class CreateTaskSchema(BaseModel):
    name: constr(max_length=128)
    description: str
    done: bool = False


class UpdateTaskSchema(BaseModel):
    name: constr(max_length=128)
    description: str
    done: bool


class ReadTaskSchema(BaseModel):
    name: constr(max_length=128)
    description: str
    done: bool
