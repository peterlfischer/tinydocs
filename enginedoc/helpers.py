import re

from enginedoc.models import User

from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest


def require_staff(handler):
    def staff_required_wrapper(request, *args, **kw):
        user = User.get_current_user()
        if not user or not user.is_staff:
            raise BadRequest('Authentication required')
        return handler(request, *args, **kw)            
    return staff_required_wrapper 

def get_object_or_404(type, primarykey):
    o = type.get(primarykey)
    if not o:
        raise NotFound("No object with that key!")
    return o

class Routes(object):
    
    def __init__(self):
        self.routes = []

    def add(self, regexp, handler):
        self.routes.append({'regexp': regexp,
                            'handler': handler})
        
    def dispatch(self, request):
        for r in self.routes:
            m = re.match(r['regexp'], request.path) 
            if m:
                args = m.groupdict()
                if args:
                    return r['handler'](request, **args)
                else:
                    return r['handler'](request)
        else:
            raise NotFound("No such resource!")

routes = Routes()

def expose(url_reg_exp):
    # remember: decorate(regexp)(function)
    def decorate(handler):
        routes.add(url_reg_exp, handler)
        return handler
    return decorate
