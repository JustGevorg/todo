# Тестовое задание "Доходъ"
## Постановка задачи: 
Создайте простое RESTFUL API для управления задачами (To-Do List). API должен поддерживать следующие операции:
- Получение списка задач (GET) 
- Создание новой задачи (POST) 
- Обновление существующей задачи (PUT) 
- Удаление задачи (DELETE)

Требования:
- Используйте Flask или FastAPI
- Храните данные в памяти (или используйте SQLite для постоянного хранения)
- Реализуйте валидацию входящих данных

Дополнительно:
- реализуйте методы REST для асинхронной обработки запросов
- на сервере один метод выполняет длительную операцию, которая занимает несколько минут:
  - реализуйте серверные методы REST, чтобы клиентские приложения могли показывать прогресс данной операции
F