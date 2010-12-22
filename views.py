#!/usr/bin/python
import os
import re

from werkzeug import Request
from werkzeug import Response
from werkzeug import redirect

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound

from helpers import get_object_or_404
from helpers import url_for
from helpers import expose
from helpers import require_staff
from helpers import STATIC_PATH
from helpers import Session
from helpers import render_template

from models import Documentation
import templates

import index as doc_index

@require_staff
def post(request):
    form = request.form
    doc = Documentation()
    doc.body     = unicode(form.get('body',''))
    doc.category = unicode(form.get('category',''))
    doc.title    = unicode(form.get('title',''))
    doc.put()
    return redirect(url_for('doc', id=doc.id))

@expose('/')
def docs(request):
    if request.method == 'GET':
        query = Session.query(Documentation).order_by(Documentation.category, Documentation.title)
        return render_template('index.html', entries=query.all())
    return post(request)

@require_staff
def put(request, doc):
    query = request.form
    doc.body     = unicode(query.get('body',''))
    doc.category = unicode(query.get('category',''))
    doc.title    = unicode(query.get('title',''))

    if doc.category and doc.title:
        Session.commit()
        return redirect(url_for('doc', id=doc.id))
    else:
        raise BadRequest("Either category or title is empty!")

def show(request, doc):
    return render_template('show.html', doc=doc)

@require_staff
def delete(request, doc):
    doc.delete()
    doc_index.delete(doc.id)
    return redirect(url_for('docs'))

@expose('/<int:id>/')
def doc(request, id):
    doc = get_object_or_404(Documentation, id)
    if request.method == "POST":
        if request.args.get('_method') == 'DELETE':
            return delete(request, doc)
        return put(request, doc)
    return show(request, doc)

@require_staff
@expose('/new/')
@expose('/<int:id>/edit/')
def form(request, id=""):
    doc = None
    if id:
        doc = get_object_or_404(Documentation, id)
        action = url_for('doc', id=id)
        return render_template('form.html', doc=doc, action=action)
    action = url_for('docs')
    return render_template('form.html', action=action, doc=None)

@expose('/<int:id>/body/')
def show_body_only(request, id=""):
    """Returns the body of a help topic."""
    o = get_object_or_404(Documentation, id)
    r = Response(templates.doc_body({'title':o.title, 'body': o.body, 'url': o.url }), 
                 content_type="text/html")
    r.headers['Cache-Control'] = 'public, max-age=max-age=31104000' # a year
    return r

@expose('/search/')
def search(request):
    query = request.args.get('q', '')
    page = request.args.get('page')
    page = int(page) if page else 1
    results = doc_index.find(q=query, page=page)
    return render_template('search.html', results=results, page=page, query=query)

def not_found(request):
    return Response(templates.not_found(), content_type="text/html")

