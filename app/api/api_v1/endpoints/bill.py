# local imports
from app.controllers.bill_controller import Bill # controller to implements
# the business logic for this endpoint
from . import bill_blueprint


# # class instantiations
bill = Bill()


# various route for bill operations

@bill_blueprint.route('/', methods=['GET'])
def get_all_bills():
    return bill.get_bills()


@bill_blueprint.route('/', methods=['POST'])
def create_bill():
    return bill.create_bill()


@bill_blueprint.route('/', methods=['PUT'])
def update_bill():
    return bill.update_bill()


@bill_blueprint.route('/', methods=['DELETE'])
def delete_bill():
    return bill.delete_bill()



