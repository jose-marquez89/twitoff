from .app import test_app

if __name__ == "__main__":
    test_app = twitoff.create_app(local=True)
    test_app.run()
