import re

from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.fields import ID

from whoosh.qparser import MultifieldParser

from os import path
from os import chown
from os import listdir
from os import mkdir

import shutil
import pwd

INDEX_PATH = path.join(path.dirname(__file__), "test_index")
INDEX_SCHEMA = Schema(
                body=TEXT(stored=True),
                title=TEXT(stored=True, field_boost=2.0),
                category=TEXT(stored=True, field_boost=2.0),
                url=ID(stored=True, unique=True),
                id=ID(stored=True, unique=True))

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
                                            
class Index(object):
    
    def __init__(self):
        self.ix = self.get_or_create_index()
        
    def add(self, **kwargs):
        """
        """
        for k,v in kwargs.iteritems():
            kwargs[k] = unicode(v)
        kwargs['body'] = strip_tags(kwargs['body']) 
        
        writer = self.ix.writer()
        # update creates or overwrites existing based on path
        writer.update_document(**kwargs)
        writer.commit()

    def delete(self, id):
        writer = self.ix.writer()
        writer.delete_document(id)
        writer.commit()
    
    def merge(self):
        self.ix.merge()

    def find(self, page=1, q=""):
        """Finds results with occurences of the query.
        """
        q = unicode(q)
        query = MultifieldParser(['body', 'title', 'category'], schema=INDEX_SCHEMA).parse(q)
        searcher = self.ix.searcher()
        return searcher.search_page(query, page)

    def get_or_create_index(self):
        if not path.exists(INDEX_PATH):
            mkdir(INDEX_PATH)
            return create_in(INDEX_PATH, INDEX_SCHEMA)
        return open_dir(INDEX_PATH)

def find(page=1, q=""):
    return Index().find(page=page, q=q)

def add(**kwargs):
    return Index().add(**kwargs)
    
def delete(id):
    return Index().delete(id)

def remove():
    if path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH)

def populate():
    from models import Documentation
    from helpers import Session
    for d in Session.query(Documentation).all():
        d.put()

def set_permissions():
    user = pwd.getpwnam('www-data')
    chown(INDEX_PATH, user.pw_uid, user.pw_gid)

    for f in listdir(INDEX_PATH):
        chown(path.join(INDEX_PATH,f), user.pw_uid, user.pw_gid)
