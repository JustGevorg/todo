from enum import StrEnum


class ExceptionsDescriptionsTemplates(StrEnum):
    task_with_name_already_exists = "Задача с названием '{task_name}' уже существует!"
    deleted_task_not_exists = "Удаляемой задачи с именем '{task_name}' не существует!"
    updated_task_not_exists = "Обновляемой задачи с именем '{task_name}' не существует!"
    tasks_not_found = "Задач не найдено"


class ApiResponsesDescriptions(StrEnum):
    task_with_name_already_exists = "Задача с таким названием  уже существует"
    task_created_successfully = "Задача успешно создана"
    tasks_not_found = ""