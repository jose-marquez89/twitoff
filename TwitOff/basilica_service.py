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
    embeddings = basiliconn().embed_sentences(sentences)
    print(type(embeddings))
    # ~ breakpoint()

    for embedding in embeddings:
        print(len(embedding))
        print(list(embedding))
        print("=============")
