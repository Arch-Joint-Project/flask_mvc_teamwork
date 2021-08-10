from flask import Blueprint

# home_blue = Blueprint('home', __name__)
get_bills_blueprint = Blueprint('get_bills', __name__)

create_bills_blueprint = Blueprint('create_bill', __name__)

update_bill_blueprint = Blueprint('update_bill', __name__)

delete_bill_blueprint = Blueprint('delete_bill', __name__)

from . import views
