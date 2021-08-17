# builtin imports
import os
# third party imports
from dotenv import load_dotenv
# local imports
from app import dotenv_path # path to the .env file declared with the app directory

# Load .env file into this file
# Making it accessible within this file
load_dotenv(dotenv_path)

# Get directory of this file
# Get absolute path of that directory
basedir = os.path.abspath(os.path.dirname(__file__))


# General Configurations Parameters
class Config:
    """
    Set Flask configuration vars from .env file
    """
    # Get the database parameters from the .env file
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Get the flask environment from the .env file
    FLASK_ENV = os.getenv("FLASK_ENV")

    # This will be overridden based on configuration settings
    DB_SERVER = ""

    # General Parameters
    # These will be overridden based on the application environment
    DEBUG = False
    DEVELOPMENT = True
    SECRET_KEY = "SECRET"
    FLASK_RUN_PORT = 6000
    TESTING = False

    # Database
    # Creating a property to load database url
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.FLASK_ENV == "testing":
            return "sqlite://" + os.path.join(basedir, "test.sqlite")
        else:
            return"postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
                user=self.DB_USER,
                pw=self.DB_PASSWORD,
                url=self.DB_SERVER,
                db=self.DB_NAME
            )

    SQLALCHEMY_TRACK_MODIFICATIONS = True


# Configuration pertaining to development
class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_SERVER = os.getenv("DEV_DB_SERVER")
    # FLASK_RUN_PORT = 6000


# Configuration pertaining to Production
class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    DB_SERVER = os.getenv("DB_SERVER")


# Configuration pertaining to Testing
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    # SQL_ALCHEMY_DATABASE_URI = "sqlite://memory:"
