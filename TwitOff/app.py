from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from TwitOff.models import db, migrate
from TwitOff.routes.tweet_routes import tweet_routes

def create_app():
    """Create and configure an instance of Flask"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/jose/Documents/lambdaRepos/twitoff/twitoff.db"
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tweet_routes)

    return app
