# local imports
from app.controllers.bill_controller import Accounts # controller to implement
# the business logic for this endpoint
from . import account_blueprint

account = Accounts()


# route for generating invoice
@account_blueprint.route('/invoice', methods=['GET'])
def generate_invoice():
    return account.generate_invoice()