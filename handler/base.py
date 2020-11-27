#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado import web
from datetime import datetime
import json


class BaseHandler(web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = self.application.redis
        self.mongo = self.application.mongo.exampledb
        self.amqp = self.application.amqp
        self.start = datetime.now()
        self.data = None
        print(f'>>> {self.start.strftime("%H:%M:%S.%f")} {self.__class__.__name__}.__init__()')

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def prepare(self):
        if (self.request.method in ['POST', 'PUT']) \
                and self.request.body:
            try:
                self.data = json.loads(self.request.body, encoding='utf-8')
            except json.decoder.JSONDecodeError as e:
                self.finish({
                    'err': 500,
                    'smg': f'data format error: {e.msg}'}
                )

    # def write_error(self, status_code, **kwargs):
    #     print(f'write_error() -> status_code={status_code}, kwargs={kwargs}')
    #     exc_info = kwargs.get('exc_info')  # <class 'HTTPError'>, <class 'HTTPError'>, <traceback>
    #     msg = exc_info[1].log_message or 'Unknown'
    #     msg = f'{self._reason} ({msg})'
    #     self.set_header('Content-Type', 'text/html; charset=UTF-8')
    #     self.finish(
    #         "<html><title>%(code)d: %(message)s</title>"
    #         "<body>%(code)d: %(message)s</body></html>"
    #         % {"code": status_code, "message": msg}
    #     )

    def on_finish(self):
        end = datetime.now()
        print(f'>>> {end.strftime("%H:%M:%S.%f")} {self.__class__.__name__}.on_finish(), '
              f'method: {self.request.method}, cost: {str(end - self.start)}')
