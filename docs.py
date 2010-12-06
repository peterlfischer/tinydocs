#!/usr/bin/python
import os
import re

from wsgiref.handlers import CGIHandler

from werkzeug import Request
from werkzeug import Response
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound

from enginedoc.helpers import get_object_or_404
from enginedoc.helpers import routes
from enginedoc.helpers import expose
from enginedoc.helpers import require_staff

from enginedoc.models import Documentation

import enginedoc.db as db
import enginedoc.templates as templates

def docs_get_handler(request):
    return Response(templates.docs({
            'docs': Documentation.find()
            .order_by(Documentation.category, Documentation.title)
            }), content_type="text/html")

@require_staff
def docs_post_handler(request):
    form = request.form
    doc = Documentation()
    doc.body     = unicode(form.get('body',''))
    doc.category = unicode(form.get('category',''))
    doc.title    = unicode(form.get('title',''))
    doc.add()
    return Response(
        '{"message": "Documentation %s added", "id": %s }' % (doc.title, doc.id),
        content_type="application/json"
        )

@expose(r'^/?$')
def docs_handler(request):
    if request.method == 'GET':
        return docs_get_handler(request)
    return docs_post_handler(request)

@expose(r'^/(?P<id>[0-9]+)/edit/?$')
@expose(r'^/new/?$')
@require_staff
def doc_form_handler(request, id=""):
    instance = None
    if id:
        instance = get_object_or_404(Documentation, int(id))
    return Response(templates.doc_form({ 'instance': instance, 'request': request }),
                    content_type="text/html")

@require_staff
def doc_put_handler(request, doc):
    query = request.form
    doc.body     = unicode(query.get('body',''))
    doc.category = unicode(query.get('category',''))
    doc.title    = unicode(query.get('title',''))

    if doc.category and doc.title:
        doc.update()
        action = doc.url
        return Response(
            '{"message": "Documentation %s updated", "action":"%s"}' % (doc.title, action),
            content_type="application/json")
    else:
        # _db.rollback()
        raise BadRequest("Either category or title is empty!")

@expose(r'^/(?P<id>[0-9]+)/?$')
def doc_handler(request, id=-1):
    o = get_object_or_404(Documentation, int(id))
    if request.method == 'POST':
        return doc_put_handler(request, o)
    return Response(templates.doc({'doc': o}), content_type="text/html")

@expose(r'^/(?P<id>[0-9]+)/body/?$')
def doc_body_handler(request, id=""):
    """Returns the body of a help topic."""
    o = get_object_or_404(Documentation, int(id))
    r = Response(templates.doc_body({'title':o.title, 'body': o.body, 'url': o.url }), 
                 content_type="text/html")
    r.headers['Cache-Control'] = 'public, max-age=max-age=31104000' # a year
    return r

@expose(r'^/(.*)$')
def search_handler(request):
    from enginedoc import search
    query = request.args.get('q', '')
    page = request.args.get('page')
    page = int(page) if page else 1
    results = search.find(q=query, page=page)
    return Response(templates.search({'results': results, 'q': query, 'page': page}),
                    content_type="text/html")

@Request.application
def app(request):
    if os.environ.get('SERVER_SOFTWARE') == "development":
        # create in memory tables
        import tests
    try:
        return routes.dispatch(request)
    except HTTPException, e:
        print e
        return e

if __name__ == '__main__':
    import cgitb; cgitb.enable()
    CGIHandler().run(app)
