import logging
from logging import FileHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from queue import Queue
from threading import Thread


class AsyncHandlerMixin(object):
    def __init__(self, *args, **kwargs):
        super(AsyncHandlerMixin, self).__init__(*args, **kwargs)
        self.__queue = Queue()
        self.__thread = Thread(target=self.__loop)
        self.__thread.daemon = True
        self.__thread.start()

    def emit(self, record):
        self.__queue.put(record)

    def __loop(self):
        while True:
            record = self.__queue.get()
            try:
                # Из очереди отправляем в ниже стоящий класс по mro().
                # Формируется из ниже скомбинированных хендлер+миксин.
                super(AsyncHandlerMixin, self).emit(record)
            except:
                # По идее тут должен быть pass, но тогда запись пропадет,
                # а так при блоке добавляем запись опять в очередь.
                # Правда так и не смог добится, что бы хоть раз сработал file_exception :).
                logging.error(f'AsyncHandlerMixin LOOP EXCEPTION - {record}')
                self.__queue.put(record)


class AsyncFileHandler(AsyncHandlerMixin, FileHandler):
    pass


class AsyncRotatingFileHandler(AsyncHandlerMixin, RotatingFileHandler):
    pass


class AsyncTimedRotatingFileHandler(AsyncHandlerMixin, TimedRotatingFileHandler):
    pass
