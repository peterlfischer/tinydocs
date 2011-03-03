import re
from flask import g
from flask import abort
from flask import redirect
from flask import url_for

from functools import wraps

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    import translitcodec
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def get_object_or_404(type, primarykey):
    from tiny import db
    o = db.query(type).get(primarykey)
    if not o:
        abort("No object with that key!")
    return o

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# def require_staff(handler):
#     def staff_required_wrapper(request, *args, **kw):
#         from models import User
#         if not is_staff():
#             raise BadRequest('Authentication required')
#         return handler(request, *args, **kw)            
#     return staff_required_wrapper

