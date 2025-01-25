class BaseTodoException(Exception):
    def __init__(self, description: str):
        self.description = description

    def __str__(self):
        return self.description


class TaskNotExistsException(BaseTodoException):
    """Задачи не существует"""

class TaskAlreadyExists(BaseTodoException):
    """Задача уже существует"""