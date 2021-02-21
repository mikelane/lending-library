import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv(".env")
load_dotenv("database.env")

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=f"postgres://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('postgres_password')}@{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('postgres_port')}/{os.getenv('postgres_db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
