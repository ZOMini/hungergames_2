import asyncio
from typing import Type

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.app import db
from db.models_db import Link, User
from tests.testdata.api_data import user_create_data


@pytest_asyncio.fixture
def db_get_user_by_name(db_client: AsyncSession):
    async def inner(name: str):
        db_obj = await db_client.scalar(select(User).filter(User.name == name))
        return db_obj
    return inner


@pytest_asyncio.fixture
def db_get_obj_by_id(db_client: AsyncSession):
    async def inner(obj: Type[User | Link], id: str):
        db_obj = await db_client.get(obj, id)
        return db_obj
    return inner


@pytest_asyncio.fixture
def db_delete_obj_by_id(db_client: AsyncSession):
    async def inner(obj: Type[User | Link], id: str):
        db_obj = await db_client.get(obj, id)
        await db_client.delete(db_obj)
        await db_client.commit()
    return inner


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clear_db(db_client: AsyncSession):
    await asyncio.sleep(3)  # Для Github Actions Workflow, иначе не успевает открыть соккеты.
    yield
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)

    async def delete_obj(obj):
        if obj:
            await db_client.delete(obj)

    db_obj = await db_client.scalar(select(User).filter(User.name == user_create_data['name']))
    await delete_obj(db_obj)
    db_obj = await db_client.scalar(select(Link).filter(Link.domain == 'abc.hostname'))
    await delete_obj(db_obj)
    db_obj = await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test'))
    await delete_obj(db_obj)
    db_obj = await db_client.scalar(select(User).filter(User.name == 'testuser2'))
    await delete_obj(db_obj)
    await db_client.commit()
    db.session.close_all()
