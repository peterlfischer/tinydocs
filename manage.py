#!/usr/bin/python
from os import environ
from werkzeug import script

environ['SERVER_SOFTWARE'] = 'development'

def make_app():
    from application import Docs
    return Docs("sqlite:///docs.db")

def make_shell():
    import models
    import helpers
    application = make_app()
    return locals()

def make_index():
    import models
    import helpers
    application = make_app()

    import index
    index.remove()
    index.populate()
    index.set_permissions()

action_initdb = lambda: make_app().init_database()
action_runserver = script.make_runserver(make_app, use_reloader=True)
action_shell = script.make_shell(make_shell)
action_index = make_index

script.run()
