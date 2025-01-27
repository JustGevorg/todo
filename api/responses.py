from resources import ApiResponsesDescriptions, ExceptionsDescriptionsTemplates

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

}