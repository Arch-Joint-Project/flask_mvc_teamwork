# local imports
# loading the blueprint and initializing with core application
from .endpoints import bill_blueprint, account_blueprint


# create a function to register all blueprints
def init_app(app):
    app.register_blueprint(bill_blueprint, url_prefix="/bill")
    app.register_blueprint(account_blueprint, url_prefix="/account")