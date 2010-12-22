import re
from os import path
from os import environ

from jinja2 import Environment
from jinja2 import FileSystemLoader

from werkzeug import Response
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest
from werkzeug.routing import Map
from werkzeug.routing import Rule

from werkzeug import Local
from werkzeug import LocalManager

from sqlalchemy import MetaData
from sqlalchemy.orm import create_session, scoped_session
from sqlalchemy.ext import declarative

STATIC_PATH = path.join(path.dirname(__file__), 'static')
TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
MOUNT_POINT = ''

local = Local()
local_manager = LocalManager([local])
application = local('application')

Base = declarative.declarative_base()

metadata = MetaData()

url_map = Map()

Session = scoped_session(lambda: create_session(application.database_engine,
                         autocommit=False, autoflush=False),
                         local_manager.get_ident)

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate

def url_for(endpoint, _external=False, **values):
    return local.url_adapter.build(endpoint, values, force_external=_external)

def is_staff():
    from models import User
    return User.is_staff()

jinja_env.globals['url_for'] = url_for
jinja_env.globals['is_staff'] = is_staff

def require_staff(handler):
    def staff_required_wrapper(request, *args, **kw):
        from models import User
        if not is_staff():
            raise BadRequest('Authentication required')
        return handler(request, *args, **kw)            
    return staff_required_wrapper

def get_object_or_404(type, primarykey):
    o = Session.query(type).get(primarykey)
    if not o:
        raise NotFound("No object with that key!")
    return o

def render_template(template, **context):
    return Response(jinja_env.get_template(template).render(**context),
                    mimetype='text/html')
