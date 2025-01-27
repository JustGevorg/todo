from resources import ApiResponsesDescriptions, ExceptionsDescriptionsTemplates
from schemas.tasks import ReadTaskSchema

example_tasks = [ReadTaskSchema(name="Подготовиться к экзамену", description="Изучить конспект", done=False).model_dump(),
                 ReadTaskSchema(name="Выбросить мусор", description="Выбросить пакет и коробки", done=True).model_dump(),]

create_new_task_responses = {
    200: {"description": ApiResponsesDescriptions.task_created_successfully,
          "content": {
              "application/json": {
                  None}
          }},
    409: {"description": ApiResponsesDescriptions.task_with_name_already_exists,
          "content": {
              "application/json": {
                  "example": {"description": ExceptionsDescriptionsTemplates.task_with_name_already_exists.format(
                      task_name="Сходить в магазин")}
              }
          }}
}

delete_task_responses = {
    404: {"description": ApiResponsesDescriptions.tasks_not_found,
          "content": {
              "application/json": {
                  "example": {"description": ExceptionsDescriptionsTemplates.updated_task_not_exists.format(
                      task_name="Сходить в магазин")}
              }
          }},
    200: {"description": ApiResponsesDescriptions.task_deleted_successfully,
          "content": {
              "application/json": {
                  None}
          }},
}

update_task_responses = {
    404: {"description": ApiResponsesDescriptions.tasks_not_found,
          "content": {
              "application/json": {
                  "example": {"description": ExceptionsDescriptionsTemplates.updated_task_not_exists.format(
                      task_name="Сходить в магазин")}
              }
          }},
    200: {"description": ApiResponsesDescriptions.task_updated_successfully,
          "content": {
              "application/json": {
                  None}
          }},
}


get_task_responses = {
    404: {"description": ApiResponsesDescriptions.tasks_not_found,
          "content": {
              "application/json": {
                  "example": {"description": ExceptionsDescriptionsTemplates.tasks_not_found}
              }
          }},
    200: {"description": ApiResponsesDescriptions.requested_tasks,
          "content": {
              "application/json": {
                  "example": example_tasks
              }
          }},
}