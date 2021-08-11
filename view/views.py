# local imports
from controller.bill_controller import Bill, Accounts
from . import bills_blueprint, accounts_blueprint

# class instantiations
bill = Bill()
account = Accounts()


# routes for viewing bills
@bills_blueprint.route('/', methods=['GET'])
def get_all_bills():
    return bill.get_bills()


@bills_blueprint.route('/create', methods=['POST'])
def create_bill():
    return bill.create_bill()


@bills_blueprint.route('/update', methods=['PUT'])
def update_bill():
    return bill.update_bill()


@bills_blueprint.route('/delete', methods=['DELETE'])
def delete_bill():
    return bill.delete_bill()


# route for generating invoice
@accounts_blueprint.route('/invoice', methods=['GET'])
def generate_invoice():
    return account.generate_invoice()

