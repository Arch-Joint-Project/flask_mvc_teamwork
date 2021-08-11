# application version
__version__ = '0.1.0'

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

# local imports
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# extensions instantiations
db = SQLAlchemy()
ma = Marshmallow()


# creating the base application
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cfg = import_string('config.DevelopmentConfig')()
    app.config.from_object(cfg)

    # initializing extensions with application
    db.init_app(app)
    ma.init_app(app)

    from models import model
    migrate = Migrate(app, db)

    # loading blueprints into applications
    from view.views import bills_blueprint
    app.register_blueprint(bills_blueprint)

    from view.views import accounts_blueprint
    app.register_blueprint(accounts_blueprint)

    return app
