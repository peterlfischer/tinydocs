from flask import Flask
import os

app = Flask('tiny')
if os.environ.get('TINYDOCS_SETTINGS'):
    # We're setting that variable in the tiny.wsgi used by apache
    # Another way to enable production state do this:
    # $ export TINYDOCS_SETTINGS=./settings.prod.cfg
    app.config.from_envvar('TINYDOCS_SETTINGS')    
else:
    app.config.from_pyfile('settings.dev.cfg')
app.config['INDEX_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'indexes', app.config['MODE'])

