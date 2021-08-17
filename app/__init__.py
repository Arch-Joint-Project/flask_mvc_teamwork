__version__ = '0.1.0'

# builtin imports
import os
# third library imports
from flask import Flask
from werkzeug.utils import import_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# Get the directory of this file
# Get the parent directory of of it (root of the application)
ROOT_DIRECTORY = os.path.join(os.path.dirname(__file__), "..")
# Get .env file path
dotenv_path = os.path.join(ROOT_DIRECTORY, ".env")

# Initialization of extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

# Load flask environment parameters from .env file
FLASK_ENV = os.getenv("FLASK_ENV") if os.getenv("FLASK_ENV") else "production"


def create_app():
    """
    Construct the core application
    """
    app = Flask(__name__, instance_relative_config=False)
    cfg = None
    # Load application configuration depending on environment setting
    if FLASK_ENV == "development":
        cfg = import_string("config.DevelopmentConfig")()
    elif FLASK_ENV == "production":
        cfg = import_string("config.ProductionConfig")()
    elif FLASK_ENV == "testing":
        cfg = import_string("config.TestingConfig")()
    # load the appropriate configuration
    app.config.from_object(cfg)

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """
    Register flask extensions
    """
    db.init_app(app)
    from .models import bill
    migrate.init_app(app, db)
    ma.init_app(app)

    return None


def register_blueprints(app):
    # from app.api.api_v1 import api
    from app.api import init_app
    init_app(app)
    return None
