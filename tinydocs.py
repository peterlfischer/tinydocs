#!/usr/bin/python
import logging
import os

from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
from flask import Response
from flask import Flask
from flask import session

import json
import forms

from config import app

from models import System
from models import Topic
from models import Error

###################
# Context processor
###################
@app.context_processor
def inject_user():
    if app.config.get('MODE') == 'development':
        if session.get('username'):
            return dict(user=session['username'], logout_url='/logout')
        else:
            return dict(login_url='/login')
    else:
        if request.environ.get('REMOTE_USER'):
            return dict(user=True)
        else:
            return dict(user=None,login_url='/admin%s' % request.path)

@app.context_processor
def inject_media_version():
    return dict(version=app.config.get('MEDIA_VERSION'))

############
# decorators
############
def login_required(fn):
    def decorated(*args, **kw):
        if request.environ.get('REMOTE_USER'):
            return fn(*args, **kw)
        if app.config.get('MODE') == 'development' and session.get('username'):
            return fn(*args, **kw)
        return Response('You need to login first!', status=400)
    return decorated

##########################
## generic helper-handlers
##########################
def get(Type=None, key_name=None, obj=None, **kwargs):
    """Gets object from database and renders html page.

    :param Type: the type of the model
    :param key_name: the key name of the model.
    """
    if not obj:
        obj = Type.query.get_or_404(key_name)
    return render_template("%s.html" % Type.__name__.lower(), o=obj, **kwargs)

@login_required
def add(Type=None, form=None, **kwargs):
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
    return render_template("%s_form.html" % Type.__name__.lower(), form=form,**kwargs)

@login_required
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
        abort(400)

@login_required
def edit(Type=None, key_name=None, form=None, **kwargs):
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
        flash('Nice, you just saved %s' % (o.name), 'message')
        return redirect(o.url)
    return render_template("%s_form.html" % Type.__name__.lower(), form=form, **kwargs)

####################
# Standard 404 page
###################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#################
# Dev. mode auth
################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if app.config.get('MODE') == 'development':
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('get_systems'))
        return '''
        <form action="" method="post">
            <p><input type="text" name="username" />
            <p><input type="submit" value="Login" />
        </form>'''
    abort(404)

@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    return redirect(url_for('get_systems'))

##################
# Admin Handlers
##################
@login_required
@app.route('/actions/reindex', methods=['POST'])
def reindex():
    import index
    index.remove()
    index.populate()
    flash('Removed existing index and created new!')
    return redirect(request.headers['referer'])
    
##################
# Systems Handlers
##################
@app.route('/', methods=['GET'])
def get_systems():
    return render_template('systems.html', systems=System.query.all())

@app.route('/<key_name>', methods=['GET'])
def get_system(key_name):
    return get(Type=System, key_name=key_name)

@app.route('/<key_name>', methods=['POST'])
def delete_system(key_name):
    url = url_for(get_systems.__name__)
    return delete(Type=System, key_name=key_name, redirect_url=url)

@app.route('/new', methods=['GET', 'POST'])
def add_system():
    return add(Type=System, form=request.form)

@app.route('/<key_name>/edit', methods=['GET', 'POST'])
def edit_system(key_name):
    return edit(Type=System, key_name=key_name, form=request.form)

#################
# Topics Handlers
#################
@app.route('/plugin/embed.js', methods=['GET'])
def get_topic_plugin():
    """Renders embed.js"""
    headers = {
        'Cache-Control': 'public, max-age=31104000', # a year
        }
    t = render_template('embed.js', host=request.environ['HTTP_HOST'])
    return Response(t, mimetype='application/javascript', headers=headers)

@app.route('/plugin/<uid>', methods=['GET'])
def get_topic_plugin_by_uid(uid):
    """Renders a tooltip button for use in iframes."""
    obj = Topic.query.filter_by(uid=uid).first_or_404()
    return render_template("topic.plugin.html", o=obj)

# For cross-site use
@app.route('/topics/<uid>/jsonp', methods=['GET'])
def get_topic_by_uid_and_jsonp(uid):
    """Gets topic by JSONP"""  
    obj = Topic.query.filter_by(uid=uid).first_or_404()
    callback = request.args.get('callback')
    data = json.dumps({'name': obj.name, 'excerpt':obj.excerpt})
    return Response(response='%s(%s)' % (callback, data), mimetype='application/json')

# For normal use
@app.route('/topics/<uid>', methods=['GET'])
def get_topic_by_uid(uid):
    obj = Topic.query.filter_by(uid=uid).first_or_404()
    host = request.environ['HTTP_HOST']
    return redirect(obj.url)

@app.route('/<system_key_name>/<category>/<name>', methods=['GET'])
def get_topic(system_key_name, category, name):
    key_name = '%s/%s/%s' % (system_key_name, category, name)
    host = request.environ['HTTP_HOST']
    return get(Type=Topic, key_name=key_name, host=host)

# @app.route('/<system_key_name>/<category>/<name>/body', methods=['GET'])
# def get_topic_body(system_key_name, category, name):
#     key_name = '%s/%s/%s' % (system_key_name, category, name)
#     obj = get(Type=Topic, key_name=key_name)
#     return """<div>
#   <h2>%s</h2>
#   <div>%s</div>
# </div>""" % (obj.name, obj.body)

@app.route('/<system_key_name>/new', methods=['GET', 'POST'])
def add_topic(system_key_name):
    form = request.form.copy()
    form['system'] = system_key_name
    system = System.query.get(system_key_name)
    return add(Type=Topic, form=form, system=system)

@app.route('/<system_key_name>/<category>/<name>', methods=['POST'])
def delete_topic(system_key_name, category, name):
    key_name = '%s/%s/%s' % (system_key_name, category, name)
    return delete(Type=Topic, key_name=key_name, redirect_url=url_for(get_system.__name__, key_name=system_key_name))

@app.route('/<system_key_name>/<category>/<name>/edit', methods=['POST','GET'])
def edit_topic(system_key_name, category, name):
    system = System.query.get_or_404(system_key_name)
    key_name = '%s/%s/%s' % (system_key_name, category, name)
    return edit(Type=Topic, key_name=key_name, form=request.form, system=system)

##########
# Search
##########
@app.route('/search/')
def search():
    import index
    query = request.args.get('q', '')
    page = request.args.get('page')
    page = int(page) if page else 1
    results = index.find(query=query, page=page)
    return render_template('search.html', results=results, page=page, query=query)

if __name__ == '__main__':
    import os
    if not os.path.exists(app.config['DATABASE_FILE']):
        from models import db
        db.create_all()
    app.run()
