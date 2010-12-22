#!/usr/bin/python
import os
import unittest
import simplejson
import shutil

from werkzeug import EnvironBuilder
from werkzeug import Request
from werkzeug import Client
from werkzeug import BaseResponse

from models import Documentation
from models import User

import index

os.environ['MODE'] = 'test'
os.environ['REMOTE_USER'] = 'dam'

index.INDEX_PATH = "test_index"

from application import Docs
app = Docs("sqlite:///docs.db")

class DocumentationHandlerTest(unittest.TestCase):

    def setUp(self):
        self.doc = Documentation()
        self.doc.category = u'acategory'
        self.doc.title = u'adoc'
        self.doc.put()
        self.c = Client(app, BaseResponse)

    def tearDown(self):
        self.doc.delete()
    
    def test_post_new_doc(self):
        r = self.c.post(
            path="/",
            data={'body': u'the body','category': u'the category','title': u'the title'}
            )
        self.assertEquals(r.status_code, 302)
        # # check index

    def test_get_edit_doc(self):
        r = self.c.get(
            path="/%s/edit/" % (self.doc.id),
            data={'id': self.doc.id}
            )
        self.assertTrue('acategory' in r.data)
        self.assertTrue('adoc' in r.data)

    def test_get_docs(self):
        r = self.c.get(path="/")
        self.assertFalse(r.data == None)
        self.assertTrue('acategory' in r.data)

    def test_put_doc(self):
        r = self.c.post(
            path="/%s/" % self.doc.id,
            data= {'body': u'new body',
                   'category': u'new category',
                   'title': u'new title'})
        self.assertEquals(r.status_code, 302)
        self.assertTrue(r.data)

    def test_get_body_doc(self):
        r = self.c.get(path="/%s/body/" % self.doc.id)
        self.assertTrue(r.data)
        self.assertTrue('adoc' in r.data)

class SearchIndexTest(unittest.TestCase):

    def setUp(self):
        # remove the index by deleting it
        if os.path.exists(index.INDEX_PATH):
            shutil.rmtree(index.INDEX_PATH)
        self.index = index.Index()

    def tearDown(self):
        pass

    def testAdd(self):
        helptext = {
            'category':"the category",
            'title':"the title",
            'body':"the body",
            'id':1
            }
        self.index.add(**helptext)
        results = self.index.find(q='body')
        self.assertEquals(results.total, 1)
        result = results[0]

        self.assertEquals(result['title'], 'the title')
        self.assertEquals(result['category'], 'the category')
        self.assertEquals(result['category'], 'the category')
        
        # adding with same id should ovewrite
        self.index.add(**helptext)
        result = self.index.find(q='body')
        self.assertEquals(result.total, 1)
        
if __name__ == '__main__':
    unittest.main()

