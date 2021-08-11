from flask import Blueprint

# home_blue = Blueprint('home', __name__)
bills_blueprint = Blueprint('bills', __name__, url_prefix='/bills')

accounts_blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')

# create_bills_blueprint = Blueprint('create_bill', __name__)
#
# update_bill_blueprint = Blueprint('update_bill', __name__)
#
# delete_bill_blueprint = Blueprint('delete_bill', __name__)

from . import views
