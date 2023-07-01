from celery import Celery

app = Celery('tasks',
             backend='redis://localhost:6379/1',
             broker='redis://localhost:6379/0',
             include=['proj.tasks'])
app.conf.update(
    result_expires=3600,
)
# app.conf.broker_url = 'pyamqp://guest@localhost//'
# app.conf.result_backend = 'redis://localhost:6379/0'
# app.conf.broker_transport_options = {'visibility_timeout': 3600}
# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],  # Ignore other content
#     result_serializer='json',
#     timezone='Europe/Moscow',
#     enable_utc=True,
# )


if __name__ == '__main__':
    app.start()