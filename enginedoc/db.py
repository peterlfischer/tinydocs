# import os

# from storm.locals import create_database
# from storm.locals import Store

# global db
# db = None

# if os.environ['SERVER_SOFTWARE'] == 'development':
#     db.set("sqlite:") # in memory db            
# else:
#     db.set("mysql://root:cabosql@localhost/steamregister")


# def get():
#     if not db:
#         raise Exception("db not set!")
#     return db

# def set(url):
#     global db
#     db = Store(create_database(url))
#     return db
