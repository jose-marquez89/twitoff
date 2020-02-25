from flask import Blueprint, jsonify, request, render_template
from TwitOff.models import db, User, Tweet
from TwitOff.twitter_service import twitter_api
from TwitOff.basilica_service import basiliconn

twitter_api_client = twitter_api()
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


@tweet_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    try:
        twitter_user = twitter_api_client.get_user(screen_name)

        # find or create database user:
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id))
        db_user.screen_name = twitter_user.screen_name
        db_user.name = twitter_user.name
        db_user.location = twitter_user.location
        db_user.followers_count = twitter_user.followers_count
        db.session.add(db_user)
        db.session.commit()

        statuses = twitter_api_client.user_timeline(
                                                screen_name,
                                                tweet_mode="extended",
                                                count=50,
                                                exclude_replies=True,
                                                include_rts=False
                                                )
        for status in statuses:
            print(status.full_text)
            print("==============")

            db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
            db_tweet.user_id = status.author.id
            db_tweet.full_text = status.full_text
            db_tweet.embedding = basilica.embed_sentence(status.full_text)

            db.session.add(db_tweet)

        db.session.commit()

        return render_template("user.html",
                               user=db_user,
                               tweets=statuses)
    except Exception:
        return jsonify({"message": "OOPS User Not Found!"})


# ~ @tweet_routes.route("/tweets/new-tweet")
# ~ def new_tweet():
    # ~ return render_template("new_tweet.html")


# ~ @tweet_routes.route("/tweets/create-new", methods=["POST"])
# ~ def create_tweet():

    # ~ new = Tweet(content=request.form["content"])
    # ~ db.session.add(new)
    # ~ db.session.commit()

    # ~ return render_template("tweet_success.html")


# ~ @tweet_routes.route("/tweets/another-tweet")
# ~ def tweet_again():
    # ~ return render_template("new_tweet.html")
