import datetime
import hashlib
import uuid
from hmac import compare_digest
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

import tldextract
from flask_login import UserMixin
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    LargeBinary,
    SmallInteger,
    String,
    exists
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship
)
from sqlalchemy.sql import func
from typing_extensions import Annotated

from core.config import settings
from db.connection_db import db_session

uuidpk = Annotated[uuid.UUID, mapped_column(
    UUID(as_uuid=True),
    default=uuid.uuid4,
    primary_key=True,
    unique=True,
    nullable=False)]
timestamp_int = Annotated[datetime.datetime, mapped_column(
    TIMESTAMP(timezone=False),
    server_default=func.current_timestamp())]


class Base(DeclarativeBase):
    pass


Base.query = db_session.query_property()


class User(MappedAsDataclass, Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[uuidpk] = mapped_column(init=False)
    name = mapped_column(String(127), unique=True, nullable=False)
    email = mapped_column(String(127), unique=True, nullable=False)
    password = mapped_column(String(127), nullable=False)

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = self.password_hash(password, email)

    def __repr__(self):
        return self.id

    def password_hash(self, password: str, email: str) -> str:
        '''Функция хеширует пароль(sha256 + стат. соль + дин. соль).'''
        pw_hash = hashlib.sha256((password + settings.app.salt_password + email).encode('utf-8')).hexdigest()
        return pw_hash

    def check_password(self, password: str, email: str) -> bool:
        '''Функция сравнивает пароли - нехешированный(in param) с хешированным(в базе).'''
        return compare_digest(self.password_hash(password, email), self.password)


class Link(MappedAsDataclass, Base):
    __tablename__ = 'links'

    id: Mapped[uuidpk] = mapped_column(init=False)
    protocol = mapped_column(String(63), nullable=False)
    domain = mapped_column(String(127), nullable=False)
    suffix = mapped_column(String(63), nullable=False)
    path = mapped_column(String(255))
    param = mapped_column(JSON(True))
    filename = mapped_column(String(50))
    filedata = mapped_column(LargeBinary)
    linkstatus = mapped_column(SmallInteger, default=200)
    available = mapped_column(Boolean, default=True)
    events: Mapped[List["Event"] | None] = relationship(back_populates='link', order_by='desc(Event.timestamp)',)
    lasttime: Mapped[timestamp_int] = mapped_column(init=False)

    def __init__(self, url: str):
        parse_object = urlparse(url)
        parse_domain = tldextract.extract(url)
        self.protocol = parse_object.scheme
        self.domain = parse_domain.subdomain + '.' + parse_domain.domain if parse_domain.subdomain else parse_domain.domain
        self.suffix = parse_domain.suffix
        self.path = parse_object.path
        self.param = parse_qs(parse_object.query)
        self.check_data()
        self.check_duplicate()

    def __repr__(self) -> str:
        return self.get_url()

    def check_data(self):
        '''Проверяет url на валидность.'''
        if not self.protocol or not self.domain or not self.suffix:
            raise ValueError('Not valid url.')

    def check_duplicate(self):
        '''Проверяет url на наличиее его в базе.'''
        if db_session.query(exists().where((Link.protocol == self.protocol) & (Link.domain == self.domain) & (Link.suffix == self.suffix) & (Link.path == self.path))).scalar():
            raise ValueError('Url is duplicate.')

    def url_query(self) -> str:
        '''Формирует строкое представление для query params.'''
        query_param_str = '?'
        for k, v in self.param.items():
            query_param_str += ('&' + k + '=' + v[0]) if len(query_param_str) > 1 else (k + '=' + v[0])
        query_param_str = query_param_str if len(query_param_str) > 1 else ''
        return query_param_str

    def get_url(self) -> str:
        '''Формирует строкое представление для всего урла. Вынес в отдельный метод.'''
        query_param_str = self.url_query()
        return f'{self.protocol}://{self.domain}.{self.suffix}{self.path}{query_param_str}'

    def get_dict(self) -> dict:
        '''Формирует дикт для ответа.'''
        return {'id': self.id,
                'protocol': self.protocol,
                'domain': self.domain,
                'suffix': self.suffix,
                'path': self.path,
                'params': self.param}


class Event(MappedAsDataclass, Base):
    __tablename__ = 'event'

    id: Mapped[uuidpk] = mapped_column(init=False)
    timestamp: Mapped[timestamp_int] = mapped_column(init=False)
    link_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("links.id", ondelete='SET NULL'), default=None)
    link: Mapped[Link | None] = relationship(back_populates="events", default=None)
    url = mapped_column(String(511), nullable=False) 
    event = mapped_column(String(511), nullable=False)

    def __repr__(self) -> str:
        return str(self.id)

    def __init__(self, url: str, event: str, link_id = None):
        self.link_id = link_id
        self.url = url
        self.event =  event
