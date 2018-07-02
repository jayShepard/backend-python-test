from flask import Flask, g
from database import db_session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


@app.before_request
def before_request():
    g.db = db_session


@app.teardown_request
def teardown_request(exception=None):
    db_session.remove()


import alayatodo.views
