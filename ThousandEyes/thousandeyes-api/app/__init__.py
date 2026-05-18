from flask import Flask

from app.routes import bp


def create_app() -> Flask:
    application = Flask(__name__)
    application.register_blueprint(bp)
    return application
