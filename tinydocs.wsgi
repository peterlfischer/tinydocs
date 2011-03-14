import os
import sys

sys.stdout = sys.stderr

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS = 'settings.prod.cfg'

sys.path.append(SITE_ROOT)

os.environ['TINYDOCS_SETTINGS'] = os.path.join(SITE_ROOT, SETTINGS)

activate_this = '/srv/www/docs.irigo.com/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from tinydocs import app as application
