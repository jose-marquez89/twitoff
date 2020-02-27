import logging
from flask import Blueprint, jsonify, request, render_template
from TwitOff.models import db, User, Tweet
from TwitOff.twitter_service import twitter_api
from TwitOff.basilica_service import basiliconn
from sklearn.linear_model import LogisticRegression

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

        # check if user is in database
        logging.info("Trying query for user...")
        if User.query.get(twitter_user.id) is None:
            user = User(id=twitter_user.id)
        else:
            return jsonify({"message": "EXISTS User Exists"})

        user.screen_name = twitter_user.screen_name
        user.name = twitter_user.name
        user.location = twitter_user.location
        user.followers_count = twitter_user.followers_count

        db.session.add(user)
        db.session.commit()

        statuses = twit_cli.user_timeline(request.form["new_user"],
                                          tweet_mode="extended",
                                          count=50,
                                          exclude_replies=True,
                                          include_rts=False)

        # zip tweets and embeddings together to improve performance
        bas_emb = basilica.embed_sentences
        status_list = [s.full_text for s in statuses]
        embedding_list = [e for e in bas_emb(status_list,
                                             model="twitter")]

        tweet_info = list(zip(statuses, embedding_list))

        for status, embedded_tweet in tweet_info:
            tweet = Tweet(id=status.id)
            tweet.user_id = status.author.id
            tweet.full_text = status.full_text
            tweet.embedding = embedded_tweet

            db.session.add(tweet)
            logging.info("Successfully completed commit.")
        db.session.commit()

        # TODO: Add a success extension for layout
        return jsonify({"message": "USER CREATED OK"})
    except Exception as err:
        requested = request.form["new_user"]
        logging.error(err)
        return jsonify({"message": f"Can't find {requested}"})


@tweet_routes.route("/users/set")
def set_users():
    user_records = User.query.all()
    return render_template("predictions.html", users=user_records)


@tweet_routes.route("/users/predict", methods=["POST"])
def predict():
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()

    X = []
    y = []
    for tweet in user_a.tweets:
        y.append(user_a.screen_name)
        X.append(tweet.embedding)

    for tweet in user_b.tweets:
        y.append(user_b.screen_name)
        X.append(tweet.embedding)

    classifier = LogisticRegression()
    classifier.fit(X, y)

    embedded_tweet = basilica.embed_sentence(tweet_text)
    prediction = classifier.predict([embedded_tweet])

    return render_template("results.html",
                           predicted=prediction[0])
