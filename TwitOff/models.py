from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# comment


db  = SQLAlchemy()

migrate = Migrate()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(208))


