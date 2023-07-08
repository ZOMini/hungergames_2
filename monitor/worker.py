import pytz  # type: ignore[import]
from apscheduler.schedulers.background import BlockingScheduler

from core.config import settings
from core.logger import console_logger
from services.worker_service import worker_run

scheduler = BlockingScheduler(timezone=pytz.utc)  # Или BackgroundScheduler
scheduler.add_job(worker_run,
                  'interval',
                  seconds=settings.app.worker.interval)
scheduler._logger = console_logger
scheduler.start()
