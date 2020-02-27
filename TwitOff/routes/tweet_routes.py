import logging
from flask import Blueprint, jsonify, request, render_template
from TwitOff.models import db, User, Tweet
from TwitOff.twitter_service import twitter_api
from TwitOff.basilica_service import basiliconn

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

twit_cli = twitter_api()
basilica = basiliconn()

tweet_routes = Blueprint("tweet_routes", __name__)


@tweet_routes.route("/users")
@tweet_routes.route("/users.json")
def list_users():
    users = []
    user_records = User.query.all()
    for user in user_records:
        print(user)
        d = user.__dict__
        del d["_sa_instance_state"]
        user.append(d)
    return jsonify(users)

@tweet_routes.route("/users/add")
def add_new():
    return render_template("add_new.html")

@tweet_routes.route("/users/request", methods=["POST"])
def request_user():

    try:
        twitter_user = twit_cli.get_user(request.form["new_user"])
        logging.info(twitter_user.id)
        # ~ breakpoint()
        # check if user is in database
        logging.info("Trying query for user...")
        if User.query.get(twitter_user.id) == None:
            user = User(id=twitter_user.id)
        else:
            return jsonify({"message": "EXISTS User Exists"})

        user.screen_name = twitter_user.screen_name
        user.name = twitter_user.name
        user.location = twitter_user.location
        user.followers_count = twitter_user.followers_count

        # ~ breakpoint()

        db.session.add(user)
        db.session.commit()

        statuses = twit_cli.user_timeline(request.form["new_user"],
                                          tweet_mode="extended",
                                          count=50,
                                          exclude_replies=True,
                                          include_rts=False)

        for status in statuses:
            tweet = Tweet(id=status.id)
            tweet.user_id = status.author.id
            tweet.full_text = status.full_text
            tweet.embedding = basilica.embed_sentence(status.full_text)

            db.session.add(tweet)
            logging.info("Successfully completed commit.")
        db.session.commit()

        # TODO: Add a success extension for layout
        return jsonify({"message": "USER CREATED OK"})
    except Exception as err:
        requested = request.form["new_user"]
        return jsonify({"message": f"Can't find {requested}"})

@tweet_routes.route("/users/set")
def set_users():
    user_records = User.query.all()
    return render_template("predictions.html", users=user_records)
# ~ @tweet_routes.route("/users/<screen_name>")
# ~ def get_user(screen_name=None):
    # ~ print(screen_name)

    # ~ try:
        # ~ twitter_user = twit_cli.get_user(screen_name)

        # ~ # find or create database user:
        # ~ db_user = (User.query.get(twitter_user.id) or
                   # ~ User(id=twitter_user.id))
        # ~ db_user.screen_name = twitter_user.screen_name
        # ~ db_user.name = twitter_user.name
        # ~ db_user.location = twitter_user.location
        # ~ db_user.followers_count = twitter_user.followers_count
        # ~ db.session.add(db_user)
        # ~ db.session.commit()

        # ~ statuses = twit_cli.user_timeline(screen_name,
                                          # ~ tweet_mode="extended",
                                          # ~ count=50,
                                          # ~ exclude_replies=True,
                                          # ~ include_rts=False)
        # ~ for status in statuses:
            # ~ print(status.full_text)
            # ~ print("==============")

            # ~ db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
            # ~ db_tweet.user_id = status.author.id
            # ~ db_tweet.full_text = status.full_text
            # ~ db_tweet.embedding = basilica.embed_sentence(status.full_text)

            # ~ db.session.add(db_tweet)

        # ~ db.session.commit()
        # ~ logging.info("Successfully completed commit.")

        # ~ return render_template("user.html",
                               # ~ user=db_user,
                               # ~ tweets=statuses)
    # ~ except Exception as err:
        # ~ return jsonify({"message": "OOPS User Not Found!",
                        # ~ "error": err})
