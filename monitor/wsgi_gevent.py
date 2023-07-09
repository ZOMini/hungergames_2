from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer

from core.app import app

WSGIServer(('127.0.0.1', 5000), app).serve_forever()
