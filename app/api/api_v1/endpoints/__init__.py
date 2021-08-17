# third party imports
from flask import Blueprint

bill_blueprint = Blueprint("bill", __name__)

account_blueprint = Blueprint("name", __name__)

from . import bill, account