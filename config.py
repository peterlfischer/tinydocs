from flask import Flask
import os
import sys

# To enable production state do this:
# $ export TINYDOCS_SETTINGS=./settings.prod.cfg

app = Flask('tiny')
if os.environ.get('TINYDOCS_SETTINGS'):
    app.config.from_envvar('TINYDOCS_SETTINGS')    
else:
    app.config.from_pyfile('settings.dev.cfg')

    
