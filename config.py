from flask import Flask
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tiny.db'

app = Flask('tiny')
app.config.from_object('config')

