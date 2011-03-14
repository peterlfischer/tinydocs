# Avoids circular dependencies to app.
import os

from flask import Flask

app = Flask('tinydocs')
if os.environ.get('TINYDOCS_SETTINGS'):
    # We're setting that variable in the tiny.wsgi used by apache
    # Another way to enable production state do this:
    # $ export TINYDOCS_SETTINGS=./settings.prod.cfg
    app.config.from_envvar('TINYDOCS_SETTINGS')    
else:
    app.config.from_pyfile('settings.dev.cfg')
    # os.environ['REMOTE_USER'] = 'foo'
