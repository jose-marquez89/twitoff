from datetime import datetime

from flask import Blueprint, request, render_template
from TwitOff.models import db, User

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/new-user")
def new_user():
    return render_template("new_user.html")

@user_routes.route("/create-new-user", methods=["POST"])
def create_user():

    new = User(username=request.form["username"], email=request.form["email"])
    db.session.add(new)
    db.session.commit()

    return render_template("congratulations.html")

