from flask import Flask

def create_app():
    """Create and configure an instance of Flask"""
    app = Flask(__name__)

    @app.route('/')
    def root():  
        return "Hola TwitOff!"

    return app 
