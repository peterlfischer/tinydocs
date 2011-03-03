#!/usr/bin/python
from os import path

from wsgiref.handlers import CGIHandler

from sqlalchemy import create_engine

from werkzeug import Request
from werkzeug import Response

from werkzeug import SharedDataMiddleware
from werkzeug import ClosingIterator
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound

from helpers import STATIC_PATH

from helpers import local
from helpers import local_manager
from helpers import url_map
from helpers import metadata
from helpers import Base

import helpers
import views

class Docs(object):

    def __init__(self, db_uri):
        local.application = self
        self.database_engine = create_engine(db_uri, convert_unicode=True)

        self.dispatch = SharedDataMiddleware(self.dispatch, {
            '/js': path.join(STATIC_PATH, 'js'),
            '/css': path.join(STATIC_PATH, 'css')
        })

    def init_database(self):
        Base.metadata.create_all(self.database_engine)        

    def dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        method = request.args.get('_method')
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except NotFound, e:
            response = views.not_found(request)
            response.status_code = 404
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                                [local_manager.cleanup])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)


if __name__ == '__main__':
    import cgitb; cgitb.enable()
    CGIHandler().run(Docs("mysql://irigo:sunshine@localhost/steamregister"))

