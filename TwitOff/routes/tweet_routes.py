from datetime import datetime

from flask import Blueprint, jsonify, request, render_template
from TwitOff.models import db, Tweet

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets/new-tweet")
def new_tweet():
    return render_template("new_tweet.html")

@tweet_routes.route("/tweets/create-new", methods=["POST"])
def create_tweet():

    new = Tweet(content=request.form["content"])
    db.session.add(new)
    db.session.commit()

    return jsonify({
        "id": "id Created",
        "content": dict(request.form)
    })


