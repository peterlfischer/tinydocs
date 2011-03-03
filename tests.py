#!/usr/bin/python
import tiny
import unittest

from models import Topic
from models import System
from models import db

class SystemsHandlerTest(unittest.TestCase):

    def setUp(self):
        tiny.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tiny.test.db'
        db.create_all()
        self.c = tiny.app.test_client()

    def tearDown(self):
        db.drop_all()

    def test_get_new_system_form(self):
        r = self.c.get(path="/new/")
        self.assertEquals(r.status_code, 200)

    def test_post_new_system(self):
        r = self.c.post(path='/new/', data={'name':'the-cool-system', 'description': 'this is a cool system'})
        self.assertEquals(r.status_code, 302)
        s = System.query.get('the-cool-system')
        self.assertEquals(s.name, 'the-cool-system')
        self.assertEquals(s.key_name, 'the-cool-system')
        self.assertEquals(s.description, 'this is a cool system')

class TopicHandlerTest(unittest.TestCase):

    def setUp(self):
        tiny.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tiny.test.db'
        db.create_all()
        self.c = tiny.app.test_client()
        System(name="asystem", description="adescription").put()


    def tearDown(self):
        db.drop_all()
    
    def test_add(self):
        r = self.c.post(path="/asystem/new/", data={'body': u'the body','category': u'the category','name': u'the name'})
        self.assertEquals(r.status_code, 302)
        # # check index

    def test_edit_form(self):
        t = Topic(name="foo", category="cat", system="asystem", body="abody").put()
        r = self.c.get(path=t.url + 'edit/')
        self.assertEquals(r.status_code, 200)
        self.assertTrue('abody' in r.data)
        self.assertTrue('foo' in r.data)
        self.assertTrue('cat' in r.data)
        self.assertTrue('asystem' in r.data)

    def test_edit(self):
        t = Topic(name="foo", category="cat", system="asystem", body="abody").put()
        r = self.c.post(path=t.url + 'edit/',
                        data={'body': u'new body','category': u'new category', 'name': u'new name'})
        self.assertEquals(r.status_code, 302)
        self.assertEquals(r.headers.get('location'), 'http://new-category/new-name/')

# class SearchIndexTest(unittest.TestCase):

#     def setUp(self):
#         # remove the index by deleting it
#         if os.path.exists(index.INDEX_PATH):
#             shutil.rmtree(index.INDEX_PATH)
#         self.index = index.Index()

#     def tearDown(self):
#         pass

#     def testAdd(self):
#         helptext = {
#             'category':"the category",
#             'title':"the title",
#             'body':"the body",
#             'id':1
#             }
#         self.index.add(**helptext)
#         results = self.index.find(q='body')
#         self.assertEquals(results.total, 1)
#         result = results[0]

#         self.assertEquals(result['title'], 'the title')
#         self.assertEquals(result['category'], 'the category')
#         self.assertEquals(result['category'], 'the category')
        
#         # adding with same id should ovewrite
#         self.index.add(**helptext)
#         result = self.index.find(q='body')
#         self.assertEquals(result.total, 1)
        
if __name__ == '__main__':
    unittest.main()

