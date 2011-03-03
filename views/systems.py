#!/usr/bin/python
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import Response
from flask import flash

from tiny import app

from models import System
from models import DBException
from helpers import slugify

import forms
import logging

##################
# /
##################
@app.route('/', methods=['GET','HEAD'])
def index():
    return render_template('index.html', systems=System.query.all())

@app.route('/new/', methods=['GET', 'POST'])
def add():
    try:
        form = forms.SystemForm(request.form)
        if form.validate_on_submit():
            s = System()
            form.populate_obj(s)
            s.key_name = slugify(form.name.data)
            s.put()
            flash('Cool, you just addded %s ' % s.name, 'message')
            return redirect('/')
    except DBException, e:
        flash(e, 'error')
    return render_template('system_form.html', form=form)

@app.route('/<system>/edit/', methods=['GET', 'POST'])
def edit(system):
    system = get_object_or_404(System, system)
    form = forms.SystemForm(request.form, system)
    if form.validate_on_submit():
        form.populate_obj(system)
        system.put()
        return redirect(url_for('/'))
    form = forms.SystemForm(request.form)
    return render_template('system_form.html', form=form)

@app.route('/search/')
def search():
    return None

if __name__ == '__main__':
    app.run()
