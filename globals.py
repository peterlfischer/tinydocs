from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
