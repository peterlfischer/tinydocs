#!/usr/bin/python
import logging

from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort

from models import Topic
from models import System
from models import Error

import forms

from config import app

###########################
## generic helper-handlers
##########################
def get(Type=None, key_name=None):
    """Gets object from database and renders html page.

    :param Type: the type of the model
    :param key_name: the key name of the model.
    """
    o = Type.query.get_or_404(key_name)
    return render_template("%s.html" % Type.__name__.lower(), o=o)

def add(Type=None, form=None):
    """Adds a new object to the database and renders page.

    :param Type: the type of the model
    :param form: the form data
    """
    try:
        form = getattr(forms, "%sForm" % Type.__name__)(form)
        if form.validate_on_submit():
            o = Type()
            form.populate_obj(o)
            o.put()
            flash('Nice, you just saved %s' % (o.name), 'message')
            return redirect(o.url)
    except Error, e:
        flash(e, 'error')
    return render_template("%s_form.html" % Type.__name__.lower(), form=form)

def delete(Type=None, key_name=None, redirect_url=None):
    """Deletes object from the database and renders page.

    :param Type: the type of the model
    :param key_name: key name of model to delete
    :param redirect_url: url to redirect to on successful save
    """
    if request.args.get('_method') == 'DELETE':
        o = Type.query.get_or_404(key_name)
        o.delete()
        flash("Sent %s down the drain!" % (o.name), 'message')
        return redirect(redirect_url)
    else:
        return abort("Yo, you can't delete with that method")

def edit(Type=None, key_name=None, form=None):
    """Edits object from the database and renders page.

    :param form: the form data
    :param Type: the type of the model
    :param key_name: key name of model to delete
    """
    o = Type.query.get_or_404(key_name)
    form = getattr(forms, "%sForm" % Type.__name__)(request.form, o)
    if form.validate_on_submit():
        form.populate_obj(o)
        o.put()
        return redirect(o.url)
    return render_template("%s_form.html" % Type.__name__.lower(), form=form)

##################
# Systems Handlers
##################
@app.route('/', methods=['GET'])
def get_systems():
    return render_template('systems.html', systems=System.query.all())

@app.route('/<key_name>/', methods=['GET'])
def get_system(key_name):
    return get(Type=System, key_name=key_name)

@app.route('/<key_name>/', methods=['POST'])
def delete_system(key_name):
    url = url_for(get_systems.__name__)
    return delete(Type=System, key_name=key_name, redirect_url=url)

@app.route('/new/', methods=['GET', 'POST'])
def add_system():
    return add(Type=System, form=request.form)

@app.route('/<key_name>/edit/', methods=['GET', 'POST'])
def edit_system(key_name):
    return edit(Type=System, key_name=key_name, form=request.form)

#################
# Topics Handlers
################
@app.route('/<system>/<path:key_name>/', methods=['GET'])
def get_topic(system, key_name):
    return get(Type=Topic, key_name=key_name)

@app.route('/<system>/new/', methods=['GET', 'POST'])
def add_topic(system):
    form = request.form.copy()
    form['system'] = system
    return add(Type=Topic, form=form)

@app.route('/<system>/<path:key_name>/', methods=['POST'])
def delete_topic(system, key_name):
    return delete(Type=Topic, key_name=key_name, redirect_url=url_for(get_system.__name__, key_name=system))

@app.route('/<system>/<path:key_name>/edit/', methods=['POST','GET'])
def edit_topic(system, key_name):
    return edit(Type=Topic, key_name=key_name, form=request.form)

##########
# Search
##########
@app.route('/search/')
def search():
    logging.info('searhing')
    import index
    query = request.args.get('q', '')
    page = request.args.get('page')
    page = int(page) if page else 1
    results = index.find(query=query, page=page)
    return render_template('search.html', results=results, page=page, query=query)

if __name__ == '__main__':
    app.run()
