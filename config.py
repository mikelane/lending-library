import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

basedir = Path(__file__).parent

load_dotenv()
load_dotenv("database.env", override=True)
load_dotenv("development.env", override=True)
load_dotenv("cicd.env", override=True)
load_dotenv("staging.env", override=True)
load_dotenv("production.env", override=True)


class Default:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Default):
    # Postgres settings for your host (AWS or whatever)
    pass


class Staging(Default):
    # Postgres settings for your host (AWS or whatever)
    pass


class Development(Default):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "Develop Secret Key"
    DB_NAME = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")


class Cicd(Default):
    DEBUG = True
    TESTING = True
    # TODO Determine the CI/CD database settings
