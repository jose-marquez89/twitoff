# Entry point for TwitOff

from .app import create_app

if __name__ == "__main__":
    twitoff = create_app()
    twitoff.run(debug=True)
