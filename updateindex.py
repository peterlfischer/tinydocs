#!/usr/bin/python
# Populates the index when starting from scratch.
import shutil
import os
import pwd

from enginedoc.models import Documentation
from enginedoc.search import INDEX_PATH

import enginedoc.db as db

def remove_index():
    if os.path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH)

def populate_index():
    for d in Documentation.find():
        d.update()

def set_permissions():
    user = pwd.getpwnam('www-data')
    os.chown(INDEX_PATH, user.pw_uid, user.pw_gid)

    for f in os.listdir(INDEX_PATH):
        os.chown(os.path.join(INDEX_PATH,f), user.pw_uid, user.pw_gid)

remove_index()
populate_index()
set_permissions()

print "index updated"
