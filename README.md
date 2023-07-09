# Monitoring(Test task)
- Задание - [Test Task](https://github.com/ZOMini/hungergames_2/blob/a57414f7e9a6d9db581f7095d8bbd175585480ff/README.md)

## Info
- Авторизация отключина, для упрощения тестирования. Включить можно в [env.yaml](https://github.com/ZOMini/hungergames_2/blob/af54f1f9d861ba34e623edd33c6b9ab78b08662b/monitor/env.yaml) {app.jwt.disabled_in_api}, все работает.
- Тестировать проще через документацию.
- Добавил динамическое обновление контента по websocket, обновляет дата контент events & logs(Работает для первых страниц пагинатора, что бы не скакало когда пошел по другим страничкам).

## Запуск
- docker-compose up --build

## Urls(EP)
- {GET} http://127.0.0.1/docs/v1  - документация
- {POST} http://127.0.0.1/api/v1/auth/user_create  - создаем пользователя
- {POST} http://127.0.0.1/api/v1/auth/login  - получаем JWT по логину/паролю
- {DELETE} http://127.0.0.1/api/v1/auth/logout
- {POST} http://127.0.0.1/api/v1/monitor/one_link
- {POST} http://127.0.0.1/api/v1/monitor/links
- {POST} http://127.0.0.1/api/v1/monitor/file_upload/{link_id}
- {GET} http://127.0.0.1/api/v1/monitor/links
- {GET} http://127.0.0.1/api/v1/monitor/logs

## Urls(web)
- http://127.0.0.1/web/  - далее все ссылки на панели навигации(создаем пользователя, логинемся, открываются все ссылки)

## Migration
- Базовые миграции - автоматом. Если нужны доп. миграции то:
  - alembic немного подкручен
  - flask db migrate -m "migration 2"
  - flask db upgrade

## Misc
- win
  - celery -A app_celery.tasks worker -P thread --loglevel=INFO
- linux
  - celery -A app_celery.tasks worker -P gevent --loglevel=INFO