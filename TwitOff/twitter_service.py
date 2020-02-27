import os

from dotenv import load_dotenv
import tweepy

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


def twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY,
                               TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN,
                          TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


if __name__ == "__main__":

    api = twitter_api()
    user = api.get_user("tferriss")
    print("USER", user)
    print(user.screen_name)
    print(user.name)
    print(user.followers_count)
