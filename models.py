#!/usr/bin/python
from datetime import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import create_engine

from sqlalchemy.orm import create_session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import dynamic_loader

from helpers import url_for
from helpers import Session
from helpers import Base

import index

class Documentation(Base):
    __tablename__ = u'documentation'

    id = Column('id', Integer, primary_key=True)
    body = Column('body', Text)
    category = Column('category', String(256))
    title = Column('title', String(256))

    def __init__(self, body=u'', category=u'', title=u''):
        self.body = body
        self.category = category
        self.title = title

    @property
    def url(self):
        return '/%s/' % self.id

    def put(self):
        Session.add(self)
        Session.commit()
        index.add(body=self.body, category=self.category, title=self.title, id=self.id, url=self.url)
        return self
        
    def delete(self):
        Session.delete(self)
        Session.commit()
        return self

    def __repr__(self):
        return '<Documentation %r %r:%r>' % (self.id, self.category, self.title)

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

