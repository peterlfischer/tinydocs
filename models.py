#!/usr/bin/python
from sqlalchemy import Column
from sqlalchemy import String
from random import sample
from random import randrange

from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError

from flaskext.sqlalchemy import SQLAlchemy
from flask import url_for

from helpers import slugify
from config import app
db = SQLAlchemy(app)

class Error(Exception):
    pass


URL_CHARS = 'abcdefghijkmpqrstuvwxyzABCDEFGHIJKLMNPQRST23456789'
def get_random_uid():
    return ''.join(sample(URL_CHARS, randrange(3, 9)))

class TinyDocsModel():

    key_name = Column('key_name', String(256), primary_key=True)
    uid = Column('uid', String(10))
    name = Column('name', String(256), nullable=False)
    created = Column('created', DateTime, default=func.current_timestamp())
    updated = Column('updated', DateTime, onupdate=func.current_timestamp())
    created_by = Column('created_by', String(70))
    updated_by = Column('updated_by', String(70))

    def __init__(self, **kwargs):
        [setattr(self, k, v) for k,v in kwargs.iteritems()]
        
    def __unicode__(self):
        name = self.name
        if name is None:
            name = u""
        return u'%s' % (name,)

    def put(self):
        try:
            self.key_name = self.get_key_name()
            if not self.is_saved():
                uid = None
                while True:
                    uid = get_random_uid()
                    if not self.__class__.query.get(uid):
                        break
                self.uid = uid
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            raise Error('Hey dude, <a href="%s">%s</a> is already present!' % (self.key_name, self.key_name))

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def is_saved(self):
        """Returns True if the model instance has been put() into the db at least once.
        """
        return self.uid != None

class Topic(TinyDocsModel, db.Model):

    __tablename__ = u'topic'
 
    body = Column('body', Text)
    system = Column('system', String(20), nullable=False)
    category = Column('category', String(256), nullable=False)
    published = Column('published', Boolean)
    login_required = Column('login_required', Boolean)

    @property
    def system_as_obj(self):
        return System.query.get(self.system)

    def get_key_name(self):
        return '%s/%s/%s' % (self.system, slugify(self.category), slugify(self.name))

    @property
    def url(self):
        return '/%s' % self.get_key_name()

    @property
    def permalink(self):
        return '/topics/%s' % self.uid

    @property
    def tooltip_permalink(self):
        return '/plugin/%s' % (self.uid)
    
    def put(self):
        import index
        super(Topic, self).put()
        index.add(body=self.body, category=self.category, name=self.name, url=self.permalink)
        return self

class System(TinyDocsModel, db.Model):

    __tablename__ = u'system'

    description = Column('description', String(256))
    icon_url = Column('icon_url', String(256))
    published = Column('published', Boolean)
    login_required = Column('login_required', Boolean)

    @property
    def topics(self):
        return Topic.query.filter_by(system=self.key_name).order_by(Topic.category)

    @property
    def url(self):
        if not self.is_saved():
            return url_for('get_system', key_name=slugify(self.name))
        return url_for('get_system', key_name=self.key_name)        

    def get_key_name(self):
        return '%s' % slugify(self.name)

class User(object):

    @classmethod
    def is_staff(self):
        return True
       
# #    CREATE TABLE documentation ( body TEXT, category VARCHAR(256),\
# #    heading VARCHAR(256), id VARCHAR(256) NOT NULL PRIMARY KEY, title VARCHAR(256) );

# class User(Model):
#     __storm_table__ = "users"

#     username = Unicode(primary=True)
#     password = Unicode()
#     fullname = Unicode()
#     privileges = Unicode()

#     @property
#     def is_staff(self):
#         return self.privileges and self.privileges.find('a') != -1

#     @classmethod
#     def get_current_user(cls):
#         username = os.environ.get('REMOTE_USER')
#         if username:
#             return get_db().get(User, unicode(username))
#         return None

# import os

# from storm.locals import Unicode
# from storm.locals import Int
# from storm.locals import create_database
# from storm.locals import Store

# from consts import PREFIXURL
# import search

# db = None

# def get_memory_db():
#     return Store(create_database("sqlite:"))

# def get_mysql_db():
#     return Store(create_database("mysql://irigo:sunshine@localhost/steamregister"))

# def get_db():
#     global db
#     if db:
#         return db
#     if os.environ.get('SERVER_SOFTWARE') == 'development' or os.environ.get('MODE') == 'test':
#         db = get_memory_db()
#     else:
#         db = get_mysql_db()
#     return db



# class Model(object):

#     @classmethod
#     def find(cls):
#         return get_db().find(cls)

#     @classmethod
#     def get(cls, key):
#         return get_db().get(cls, key)

#     def add(self):
#         db = get_db()
#         db.add(self)
#         db.commit()

#     def update(self):
#         db.commit()
    
# class Documentation(Model):
#     __storm_table__ = "documentation"

#     id = Int(primary=True)
#     body = Unicode()
#     category = Unicode()
#     title = Unicode()

#     def str(self):
#         return "%s %s" % (self.category, self.title)

#     @property
#     def url(self):
#         return "%s%s/" % (PREFIXURL, self.id)
        
#     def add(self):
#         super(Documentation, self).add()
#         search.add(body=self.body, category=self.category, title=self.title, id=self.id, url=self.url)

#     def update(self):
#         super(Documentation, self).update()
#         search.add(body=self.body, category=self.category, title=self.title, id=self.id, url=self.url)
        
# #    CREATE TABLE documentation ( body TEXT, category VARCHAR(256),\
# #    heading VARCHAR(256), id VARCHAR(256) NOT NULL PRIMARY KEY, title VARCHAR(256) );

# class User(Model):
#     __storm_table__ = "users"

#     username = Unicode(primary=True)
#     password = Unicode()
#     fullname = Unicode()
#     privileges = Unicode()

#     @property
#     def is_staff(self):
#         return self.privileges and self.privileges.find('a') != -1

#     @classmethod
#     def get_current_user(cls):
#         username = os.environ.get('REMOTE_USER')
#         if username:
#             return get_db().get(User, unicode(username))
#         return None
    
# if __name__ == '__main__':
#     pass
# #import db
# #    _db = db.set("sqlite:data/db")
# #    _db.execute("DROP TABLE topic")
# #    Topic.create_table()

