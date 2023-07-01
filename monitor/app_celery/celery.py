from celery import Celery

from core.config import settings

app = Celery('tasks',
             broker=f'{settings.redis.url}/2',
             include=['app_celery.tasks', ],
             broker_connection_retry_on_startup=True,
             broker_connection_max_retries=10)
app.conf.update(result_expires=3600 )


if __name__ == '__main__':
    app.start()
