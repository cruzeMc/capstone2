#!flask/bin/python
from config import SQLALCHEMY_DATABASE_URI
from app import db

db.create_all()