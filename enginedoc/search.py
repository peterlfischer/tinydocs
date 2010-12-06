import re

from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema
from whoosh.fields import TEXT
from whoosh.fields import ID

from whoosh.qparser import MultifieldParser

import os.path

INDEX_PATH = "index"
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
        
    def find(self, page=1, q=""):
        """Finds results with occurences of the query.
        """
        q = unicode(q)
        query = MultifieldParser(['body', 'title', 'category'], schema=INDEX_SCHEMA).parse(q)
        searcher = self.ix.searcher()
        return searcher.search_page(query, page)

    def get_or_create_index(self):
        if not os.path.exists(INDEX_PATH):
            os.mkdir(INDEX_PATH)
            return create_in(INDEX_PATH, INDEX_SCHEMA)
        return open_dir(INDEX_PATH)

def find(page=1, q=""):
    return Index().find(page=page, q=q)

def add(**kwargs):
    return Index().add(**kwargs)
    
