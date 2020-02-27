from flask import Blueprint, render_template, jsonify
from TwitOff.models import db

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def index():
    return render_template("home.html")


@home_routes.route("/reset")
def reset_db():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "DB RESET OK"})
