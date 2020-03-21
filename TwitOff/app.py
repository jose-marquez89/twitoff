import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from TwitOff.models import db, migrate
from TwitOff.routes.tweet_routes import tweet_routes
from TwitOff.routes.home_routes import home_routes
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SQLITE_URL = os.getenv("SQLITE_URL")


def create_app(local=False): 
    """Create and configure an instance of Flask
    
    Keyword Arguments:
    local -- Default is False, if True creates a local
             testing version of the application using 
             a sqlite database.
    """
    app = Flask(__name__)
    
    if local:
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_URL
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tweet_routes)
    app.register_blueprint(home_routes)

    return app


twitoff = create_app()
test_app = create_app(local=True)