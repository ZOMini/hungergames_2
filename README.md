# Monitoring(Test task)
- Задание - [Test Task]()

## Info
- Успел только backend. На flask первый опыт.
- Front буду делать, но уже после дедлайна, видимо для себя:).
- Авторизация отключина, для упрощения тестирования. Включить можно в env.yaml {app.jwt.disabled_in_api}, все работает.
- Тестировать проще через документацию.

## Запуск
- docker-compose up --build

## Urls(EP)
- {GET} http://127.0.0.1/docs/v1  - документация
- {POST} http://127.0.0.1/api/v1/auth/user_create  - создаем пользователя
- {POST} http://127.0.0.1/api/v1/auth/login  - логинемся по логину/паролю
- {DELETE} http://127.0.0.1/api/v1/auth/logout
- {POST} http://127.0.0.1/api/v1/monitor/one_link
- {POST} http://127.0.0.1/api/v1/monitor/links
- {POST} http://127.0.0.1/api/v1/monitor/file_upload/{link_id}
- {GET} http://127.0.0.1/api/v1/monitor/links
- {GET} http://127.0.0.1/api/v1/monitor/logs

## Migration
- Базовые миграции - автоматом. Если нужны доп. миграции то:
  - flask db migrate -m "migration 2"
  - flask db upgrade
