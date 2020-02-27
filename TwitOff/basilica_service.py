import os

import basilica
from dotenv import load_dotenv

load_dotenv()

BASILICA_KEY = os.getenv("BASILICA_KEY")


def basiliconn():
    connection = basilica.Connection(BASILICA_KEY)

    return connection


if __name__ == "__main__":

    sentences = ["Hello world", "What's up"]
    embeddings = [
        i for i in basiliconn().embed_sentences(sentences,
                                                model="twitter")
    ]
    both = list(zip(sentences, embeddings))

    def to_dict(zipped):
        new = {}
        for s, e in zipped:
            new[s] = e

        return new

    print(to_dict(both))
