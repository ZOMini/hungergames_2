import asyncio

import aiohttp

from core.config import settings


def get_http_client() -> aiohttp.ClientSession:
    client = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(
            None,
            connect=settings.app.worker.http_timeout,
            sock_read=settings.app.worker.http_timeout,
            sock_connect=settings.app.worker.http_timeout),
        connector=aiohttp.TCPConnector(
            limit=1024,
            loop=asyncio.get_event_loop(),
            keepalive_timeout=1.0,
            ssl=True))
    return client
