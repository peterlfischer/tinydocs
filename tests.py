#!/usr/bin/python
import os
import unittest
import docs
import simplejson
import shutil

from werkzeug import EnvironBuilder
from werkzeug import Request

from storm.locals import create_database
from storm.locals import Store

from enginedoc.models import Documentation
from enginedoc.models import User
from enginedoc.models import get_db

from enginedoc.helpers import routes

from enginedoc.consts import PREFIXURL
from enginedoc import search

import docs

os.environ['MODE'] = 'test'
os.environ['REMOTE_USER'] = 'dam'

db = get_db()
search.INDEX_PATH = "test_index"

def create_tables():
    create_doc = "CREATE TABLE documentation (\
body VARCHAR,\
category VARCHAR,\
id INTEGER PRIMARY KEY AUTOINCREMENT,\
title VARCHAR\
)"
    db.execute(create_doc)

    create_users = "CREATE TABLE users (\
username VARCHAR PRIMARY KEY,\
password VARCHAR,\
fullname VARCHAR,\
privileges VARCHAR\
)"
    db.execute(create_users)

create_tables()

class DocumentationHandlerTest(unittest.TestCase):

    def setUp(self):
        self.doc = Documentation()
        self.doc.category = u'acategory'
        self.doc.title = u'adoc'
        db.add(self.doc)

        self.user = User()
        self.user.username = u'dam'
        self.user.privileges = u'a'
        db.add(self.user)
        db.commit()

    def tearDown(self):
        db.remove(self.doc)
        db.remove(self.user)
        db.commit()
    
    def test_post_new_doc(self):
        builder = EnvironBuilder(
            path="/",
            method='POST',
            data={'body': u'the body','category': u'the category','title': u'the title'}
            )
        request = Request(environ=builder.get_environ())
        response = routes.dispatch(request).data
        self.assertTrue("Documentation the title added" in response)
        id = simplejson.loads(response)['id']
        doc = db.get(Documentation, int(id))
        self.assertFalse(doc == None)
        self.assertEquals(doc.body, u'the body')
        self.assertEquals(doc.category, u'the category')

        # check index
        

    def test_get_edit_doc(self):
        builder = EnvironBuilder(
            path="/%s/edit/" % (self.doc.id),
            data={'id': self.doc.id},
            method='GET',
            )
        request = Request(environ=builder.get_environ())
        response = routes.dispatch(request).data
        self.assertFalse(response == None)
        self.assertTrue('acategory' in response)
        self.assertTrue('adoc' in response)

    def test_get_docs(self):
        builder = EnvironBuilder()
        request = Request(environ=builder.get_environ())
        response = routes.dispatch(request).data
        self.assertFalse(response == None)
        self.assertTrue('acategory' in response)

    def test_put_doc(self):
        builder = EnvironBuilder(
            path="/%s/" % self.doc.id,
            data= {'body': u'new body',
                   'category': u'new category',
                   'title': u'new title'},
            method='POST')
        request = Request(environ=builder.get_environ())
        response = routes.dispatch(request).data
        self.assertTrue(response)
        obj = simplejson.loads(response)
        self.assertEquals(obj['message'], 'Documentation new title updated')
        self.assertEquals(obj['action'], PREFIXURL + str(self.doc.id) + '/')

    def test_get_body_doc(self):
        builder = EnvironBuilder(
            path="/%s/body/" % self.doc.id,
            method='GET')
        request = Request(environ=builder.get_environ())
        response = routes.dispatch(request).data
        self.assertTrue(response)
        self.assertTrue('adoc' in response)

class SearchIndexTest(unittest.TestCase):

    def setUp(self):
        # remove the index by deleting it
        if os.path.exists(search.INDEX_PATH):
            shutil.rmtree(search.INDEX_PATH)
        self.index = search.Index()

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

