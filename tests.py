#!/usr/bin/python
import os
import shutil
import unittest

import index
import tinydocs

from models import Topic
from models import System
from models import db

META_DESCRIPTION = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut odio. Nam sed est. Nam a risus et est iaculis adipiscing. Vestibulum ante ipsum primis in"

class SystemsHandlerTest(unittest.TestCase):

    def setUp(self):
        tinydocs.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tinydocs.test.db'
        db.create_all()
        self.c = tinydocs.app.test_client()

    def tearDown(self):
        db.drop_all()

    def test_get_new_system_form(self):
        r = self.c.get(path="/new",
                       environ_overrides={'REMOTE_USER':'admin'}
                       )
        self.assertEquals(r.status_code, 200)

    def test_post_new_system_when_logged_in(self):
        r = self.c.post(path='/new', 
                        environ_overrides={'REMOTE_USER':'admin'}, 
                        data={'name':'the-cool-system', 
                              'description': 'this is a cool system',
                              'meta_description':META_DESCRIPTION})
        self.assertEquals(r.status_code, 302)
        s = System.query.get('the-cool-system')
        self.assertEquals(s.name, 'the-cool-system')
        self.assertEquals(s.key_name, 'the-cool-system')
        self.assertEquals(s.description, 'this is a cool system')

    def test_post_new_system_when_not_logged_in(self):
        r = self.c.post(path='/new', data={'name':'the-cool-system', 'description': 'this is a cool system'})
        self.assertEquals(r.status_code, 400)

class TopicHandlerTest(unittest.TestCase):

    def setUp(self):
        tinydocs.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tinydocs.test.db'
        db.create_all()
        self.c = tinydocs.app.test_client()
        System(name="asystem", description="adescription").put()

    def tearDown(self):
        db.drop_all()
    
    def test_add(self):
        r = self.c.post(path="/asystem/new", 
                        environ_overrides={'REMOTE_USER':'admin'}, 
                        data={'body': u'the body',
                              'category': u'the category', 
                              'excerpt':u'foo', 
                              'name': u'the name',
                              'meta_description': META_DESCRIPTION})
        self.assertEquals(r.status_code, 302)
        # # check index

    def test_edit_form(self):
        t = Topic(name="foo", category="cat", system="asystem", body="abody", meta_description=META_DESCRIPTION).put()
        r = self.c.get(path='/asystem/cat/foo/edit', environ_overrides={'REMOTE_USER':'admin'})
        self.assertEquals(r.status_code, 200)
        self.assertTrue('abody' in r.data)
        self.assertTrue('foo' in r.data)
        self.assertTrue('cat' in r.data)
        self.assertTrue('asystem' in r.data)

    def test_edit(self):
        t = Topic(name="foo", category="cat", system="asystem", body="abody").put()
        r = self.c.post(path='/asystem/cat/foo/edit',
                        environ_overrides={'REMOTE_USER':'admin'},
                        data={'body': u'new body',
                              'category': u'new category', 
                              'name': u'new name',
                              'excerpt':'foo',
                              'meta_description':META_DESCRIPTION})
        self.assertEquals(r.status_code, 302)
        self.assertTrue('/new-category/new-name' in r.headers.get('location'))

    def test_get_topic_by_uid_and_jsonp(self):
        t = Topic(name="foobar", category="cat", system="asystem", body="", excerpt="abody").put()
        r = self.c.get(path='/topics/' + t.uid + '/jsonp?callback=foo')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.data, 'foo({"excerpt": "abody", "name": "foobar"})')

class SearchIndexTest(unittest.TestCase):

    def setUp(self):
        # remove the index by deleting it
        if os.path.exists(tinydocs.app.config['INDEX_FOLDER']):
            shutil.rmtree(tinydocs.app.config['INDEX_FOLDER'])

    def tearDown(self):
        pass

    def testAdd(self):
        helptext = {
            'category':"the category",
            'name':"the title",
            'body':"the body",
            'url': "/cat/name/"
            }
        index.add(**helptext)
        results = index.find(query='body')
        self.assertEquals(results.total, 1)
        result = results[0]

        self.assertEquals(result['name'], 'the title')
        self.assertEquals(result['category'], 'the category')
        
        # adding with same id should ovewrite
        index.add(**helptext)
        result = index.find(query='body')
        self.assertEquals(result.total, 1)

    def test_strip_scripts(self):
        html = index.strip_scripts('foo<script>fdasfd</script>bar')
        self.assertEquals(html, 'foobar')

class UploadHandlerTest(unittest.TestCase):

    def setUp(self):
        self.c = tinydocs.app.test_client()

    def test_get_upload_page(self):
        r = self.c.get(path='/upload/', environ_overrides={'REMOTE_USER':'admin'})
        self.assertEquals(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()

