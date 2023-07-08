import asyncio
import datetime
import logging
from http import HTTPStatus
from typing import Sequence

import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.http_client import get_http_client
from core.logger import console_logger, file_logger
from db.connection_db import get_db_contextmanager
from db.models_db import Event, Link


class WorkerService:
    '''Напрашивалось сделать воркер через Celery,
    но через asyncio удобнее, да и масштабировать проще.'''
    def __init__(self,
                 db_session: AsyncSession,
                 http_session: aiohttp.ClientSession):
        self.db_session = db_session
        self.http_session = http_session
        self.result = {'2**': 0, '!=2**': 0, 'exception': 0, 'deleted': 0}

    async def check_lasttime(self, link: Link) -> bool:
        delta_time = datetime.timedelta(minutes=settings.app.worker.time_of_unavailability)
        if link.lasttime + delta_time < datetime.datetime.utcnow():
            self.db_session.add(Event(url=link.get_url(), event='url deleted'))
            await self.db_session.delete(link)
            self.result['deleted'] += 1
            file_logger.info('Link %s delete', link)
            return False
        return True

    async def check_links(self, links: Sequence[Link]) -> list[Link]:
        '''Удаляет из БД и дальнейших операций "просроченные" ссылки.'''
        return [link for link in links if await self.check_lasttime(link)]

    async def work_with_link(self, link: Link) -> tuple:
        url = link.get_url()
        try:
            async with self.http_session.get(url) as r:
                # При редиректах все равно прилетает 200. Но < 400 на всякий.
                if r.status != link.linkstatus:
                    self.db_session.add(Event(link_id=link.id, url=link.get_url(), event=f'url has changed its status - {r.status}'))
                if r.status < 400:
                    link.available = True
                    link.linkstatus = r.status
                    link.lasttime = datetime.datetime.utcnow()
                    self.result['2**'] += 1
                    file_logger.info('Link %s available and update', url)
                    status = r.status
                else:
                    link.available = False
                    link.linkstatus = r.status
                    file_logger.info('Link %s unavailable status %s', url, r.status)
                    self.result['!=2**'] += 1
                    status = r.status
        except Exception as e:
            if link.linkstatus == HTTPStatus.OK:
                self.db_session.add(Event(link_id=link.id, url=link.get_url(), event=f'url has changed its status - 500'))
            file_logger.info('Link %s exception', url)
            link.available = False
            link.linkstatus = HTTPStatus.INTERNAL_SERVER_ERROR
            self.result['exception'] += 1
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        return status, url

    async def run_tasks(self) -> dict:
        list_ids = (await self.db_session.scalars(select(Link))).all()
        clean_list = await self.check_links(list_ids)
        await self.db_session.commit()
        if not clean_list:
            return {}
        tasks = [asyncio.ensure_future(
                 self.work_with_link(link)) for link in clean_list]
        done, _ = await asyncio.wait(tasks)
        result = {str(d.result()[1]): int(d.result()[0]) for d in done}
        await self.db_session.commit()
        # Два варианта отчета воркера, полный в консоль, общий в файл,
        # т.к. в файле есть отдельные отчеты по каждому урлу.
        file_logger.info('Worker has completed the work: %s', str(self.result).replace(',', '  | '))
        console_logger.info('Worker has completed the work: %s \nRESULT: %s', result, self.result)
        return result


async def run_works_async():
    async with get_http_client() as http_session:
        async with get_db_contextmanager() as db_session:
            worker_service = WorkerService(db_session, http_session)
            result = await worker_service.run_tasks()
            return result


def worker_run():
    asyncio.run(run_works_async())
