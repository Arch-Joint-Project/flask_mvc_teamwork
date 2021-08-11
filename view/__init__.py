# third party import
from flask import Blueprint

# blue prints for application component
bills_blueprint = Blueprint('bills', __name__, url_prefix='/bills')

accounts_blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')

from . import views
