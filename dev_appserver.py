#!/usr/bin/python
import os
os.environ['SERVER_SOFTWARE'] = 'development'

from werkzeug import run_simple
from application import application

run_simple('localhost', 5000, application, use_debugger=False, 
           use_reloader=True, threaded=False, processes=1)
