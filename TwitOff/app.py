import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from TwitOff.models import db, migrate
from TwitOff.routes.tweet_routes import tweet_routes
from TwitOff.routes.home_routes import home_routes
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = os.getenv("SQLITE_PATH")

def create_app():
    """Create and configure an instance of Flask"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tweet_routes)
    app.register_blueprint(home_routes)

    return app

twitoff = create_app()
