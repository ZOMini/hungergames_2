import logging

from gevent import monkey

result = monkey.patch_all()
logging.warning('Gevent result is %s', result)

from app import app
