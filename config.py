from flask import Flask
import os
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tiny.db'
INDEX_PATH = os.path.join(os.path.dirname(__name__), 'test_index') 

app = Flask('tiny')
app.config.from_object('config')

