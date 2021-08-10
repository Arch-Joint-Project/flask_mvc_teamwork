# application version
__version__ = '0.1.0'

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# extensions initializations
db = SQLAlchemy()
ma = Marshmallow()


# creating the base application
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_name)
    db.init_app(app)
    ma.init_app(app)

    from models import model
    migrate = Migrate(app, db)

    # loading blueprints into applications
    from view.views import get_bills_blueprint

    app.register_blueprint(get_bills_blueprint, url_prefix='/bills')

    from view.views import create_bills_blueprint

    app.register_blueprint(create_bills_blueprint, url_prefix='/create-bill')

    from view.views import update_bill_blueprint

    app.register_blueprint(update_bill_blueprint, url_prefix='/update-bill')

    from view.views import delete_bill_blueprint

    app.register_blueprint(delete_bill_blueprint, url_prefix='/delete-bill')

    return app
