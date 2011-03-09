import re
import logging

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


from config import app
INDEX_PATH = app.config.get('INDEX_PATH')
import shutil
import pwd

index_schema = Schema(
    name=TEXT(stored=True, field_boost=2.0),
    category=TEXT(stored=True, field_boost=2.0),
    body=TEXT(stored=True),
    url=ID(stored=True, unique=True),
    )

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)
                                            
class Index(object):
    
    def __init__(self):
        self.ix = self.get_or_create_index()
        
    def add(self, **kwargs):
        for k,v in kwargs.iteritems():
            kwargs[k] = unicode(v)
        kwargs['body'] = strip_tags(kwargs['body']) 
        
        writer = self.ix.writer()
        # update creates or overwrites existing based on path
        writer.update_document(**kwargs)
        writer.commit()

    def delete(self, key_name):
        writer = self.ix.writer()
        writer.delete_document(key_name)
        writer.commit()
    
    def merge(self):
        self.ix.merge()

    def find(self, page=1, query=""):
        query = unicode(query)
        query = MultifieldParser(['body', 'name', 'category'], schema=index_schema).parse(query)
        searcher = self.ix.searcher()
        return searcher.search_page(query, page)

    def get_or_create_index(self):
        if not path.exists(INDEX_PATH):
            mkdir(INDEX_PATH)
            return create_in(INDEX_PATH, index_schema)
        return open_dir(INDEX_PATH)

# useful shortcuts

def find(page=1, query=""):
    """Finds results with occurences of the query.

    :param page: the page number to retrieve
    :param q: query string
    """
    return Index().find(page=page, query=query)

def add(**kwargs):
    """Adds a topic to the index.

    :param kwargs: values to add
    """
    return Index().add(**kwargs)
    
def delete(url):
    """Delete a topic from the index.

    :param url: url of topic to delete
    """
    return Index().delete(id)

def remove():
    """Removed index

    """
    if path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH)

def populate():
    from models import Topic
    for d in Topic.query.all():
        d.put()

def set_permissions():
    user = pwd.getpwnam('www-data')
    chown(INDEX_PATH, user.pw_uid, user.pw_gid)

    for f in listdir(INDEX_PATH):
        chown(path.join(INDEX_PATH,f), user.pw_uid, user.pw_gid)
