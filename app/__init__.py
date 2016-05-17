from flask import Flask, render_template, session
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from flask.ext.login import LoginManager
from werkzeug import secure_filename
import flask_sijax
from flask_sijax import sijax
import os
import uuid

UPLOAD_FOLDER = 'app/static/profile_pics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://capstoneproject:success@localhost/capstonedb'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.secret_key = str(uuid.uuid4())
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)

app.jinja_env.add_extension('jinja2.ext.do')

from app import views, models