import logging
import os
import shlex
import subprocess

from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

result = load_dotenv()
result = load_dotenv("development.env")
result = load_dotenv("testing.env", override=True)
result = load_dotenv("staging.env", override=True)
result = load_dotenv("production.env", override=True)

db = SQLAlchemy()
ma = Marshmallow()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(os.getenv("APP_SETTINGS"))
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    ma.init_app(app)

    # a simple page that says hello
    @app.route("/health-check")
    def health_check():  # pragma: no cover
        cmd = "git describe --always"
        current_rev = subprocess.check_output(shlex.split(cmd)).strip()
        return current_rev

    return app
