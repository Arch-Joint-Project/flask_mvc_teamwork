from controller.bill_controller import Bill, Accounts
from . import bills_blueprint, accounts_blueprint

# create = CreateBill()
bill = Bill()
account = Accounts()
# update = UpdateBill()
# delete = DeleteBill()


# routes for viewing bills
@bills_blueprint.route('/', methods=['GET'])
def get_all_bills():
    return bill.get_bills()


@bills_blueprint.route('/create', methods=['POST'])
def create_bill():
    print('create post')
    return bill.create_bill()


@bills_blueprint.route('/update', methods=['PUT'])
def update_bill():
    print('update bill')
    return bill.update_bill()


@bills_blueprint.route('/delete', methods=['DELETE'])
def delete_bill():
    print('delete route')
    return bill.delete_bill()


@accounts_blueprint.route('/invoice', methods=['GET'])
def generate_invoice():
    print('accounts')
    return account.generate_invoice()

# # route for creating bills
# @create_bills_blueprint.route('/', methods=['POST'])
# def create_new_bill():
#     return create.create_bill()
#
#
# # route for updating bills
# @update_bill_blueprint.route('/<int:id>/<company>', methods=['PUT'])
# def update_bill(id, company):
#     return update.update_bill(id, company)
#
#
# # routes for deleting bills
# @delete_bill_blueprint.route('/<int:id>/<company>', methods=['DELETE'])
# def delete_bill(id, company):
#     return delete.delete_bill(id, company)
#
#
# @delete_bill_blueprint.route('/<int:id>', methods=['DELETE'])
# def delete_employee_bills(id):
#     return delete.delete_employee_bills(id)
#
#
# @delete_bill_blueprint.route('/<company>', methods=["DELETE"])
# def delete_company_bills(company):
#     return delete.delete_company_bills(company)
