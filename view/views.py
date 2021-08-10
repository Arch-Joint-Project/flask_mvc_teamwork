from controller.bill_controller import CreateBill, DeleteBill, UpdateBill, GetBills
from . import (
    get_bills_blueprint,
    create_bills_blueprint,
    update_bill_blueprint,
    delete_bill_blueprint
)

create = CreateBill()
read = GetBills()
update = UpdateBill()
delete = DeleteBill()


# routes for viewing bills
@get_bills_blueprint.route('/', methods=['GET'])
def get_all_bills():
    return read.get_all_bills()


@get_bills_blueprint.route('/<int:id>', methods=['GET'])
def get_employee_bills(id):
    return read.get_all_employee_bills(id)


@get_bills_blueprint.route('/<int:id>/<company>', methods=['GET'])
def get_employee_company_bills(id, company):
    return read.get_employee_company_bills(id, company)


@get_bills_blueprint.route('/<company>', methods=['GET'])
def get_company_bills(company):
    return read.get_company_bills(company)


# route for creating bills
@create_bills_blueprint.route('/', methods=['POST'])
def create_new_bill():
    return create.create_bill()


# route for updating bills
@update_bill_blueprint.route('/<int:id>/<company>', methods=['PUT'])
def update_bill(id, company):
    return update.update_bill(id, company)


# routes for deleting bills
@delete_bill_blueprint.route('/<int:id>/<company>', methods=['DELETE'])
def delete_bill(id, company):
    return delete.delete_bill(id, company)


@delete_bill_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_employee_bills(id):
    return delete.delete_employee_bills(id)


@delete_bill_blueprint.route('/<company>', methods=["DELETE"])
def delete_company_bills(company):
    return delete.delete_company_bills(company)
