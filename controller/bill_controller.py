# third party imports
from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

# local imports
from models.model import BillableHourModel, BillableHourSchema
from app import db
from collections import defaultdict


class CreateBill:
    def __init__(self):
        pass

    def create_bill(self):
        """
        Create bills for various companies
        """
        if request.method == 'POST':
            bill_info = request.form
            try:
                bill = BillableHourModel(
                    employee_id=bill_info['employee_id'],
                    billable_rate=bill_info['billable_rate'],
                    company=bill_info['company'],
                    date=bill_info['date'],
                    start_time=bill_info['start_time'],
                    end_time=bill_info['end_time']
                )
                db.session.add(bill)
                db.session.commit()
                return make_response(jsonify(bill_info))
            except SQLAlchemyError as e:
                return make_response(jsonify({'error': 'Error Inserting Data'}))
        else:
            return make_response(jsonify({'error': 'Invalid Request'}))


class UpdateBill:
    def __init__(self):
        pass

    def update_bill(self, emp_id, company):
        """
        Update bill of a specific company
        """
        if request.method == 'PUT':
            bill_info = BillableHourModel.query.filter_by(id=emp_id, company=company).first()
            if bill_info:
                bill_info.company = request.form['company']
                bill_info.date = request.form['date']
                bill_info.start_time = request.form['start_time']
                bill_info.end_time = request.form['end_time']
                bill_info.billable_rate = request.form['billable_rate']
                db.session.commit()
                return make_response(jsonify({"status": "Successful"}))
            else:
                return make_response(jsonify({'error': 'Records Not Found'}))
        else:
            return make_response(jsonify({'error': 'Invalid Request'}))


class DeleteBill:
    def __init__(self):
        pass

    def delete_bill(self, emp_id, company):
        """
        Delete bill created by a specific employee
        for a specific company
        """
        if request.method == 'DELETE':
            bill_info = BillableHourModel.query.filter_by(id=emp_id, company=company).first()
            if bill_info:
                db.session.delete(bill_info)
                db.session.commit()
                return make_response(jsonify({"status": "Successful"}))
            else:
                return make_response(jsonify({'status': 'Operation failed', 'error': 'Record Not Found'}))
        else:
            return make_response(jsonify({'error': 'Invalid Request'}))

    def delete_company_bills(self, company):
        """
        Delete bills of a specific company
        """
        if request.method == 'DELETE':
            bill_info = BillableHourModel.query.filter_by(company=company).all()
            if bill_info:
                for m in bill_info:
                    db.session.delete(m)
                    db.session.commit()
                return make_response(jsonify({"status": "Opretion Successful"}))
            else:
                return make_response(jsonify({'status': 'Operation failed', 'error': 'Record Not Found'}))
        else:
            return make_response(jsonify({'error': 'Invalid Request'}))

    def delete_employee_bills(self, emp_id):
        """
        Delete bills of a specific employee
        """
        if request.method == 'DELETE':
            bill_info = BillableHourModel.query.filter_by(id=emp_id).all()
            if bill_info:
                for m in bill_info:
                    db.session.delete(m)
                    db.session.commit()
                return make_response(jsonify({"status": "Operation Successful"}))
            else:
                return make_response(jsonify({'status': 'Operation failed', 'error': 'Record Not Found'}))
        else:
            return make_response(jsonify({'error': 'Invalid Request'}))


class GetBills:
    def __init__(self):
        pass

    def get_all_bills(self):
        """
        Retrieve all available bills
        """
        billable_schema = BillableHourSchema()
        bills = billable_schema.dump(BillableHourModel.query.all(), many=True)
        return make_response(jsonify(bills))

    def get_all_employee_bills(self, emp_id):
        """
        Retrieve bills of a specific employee
        """
        billable_schema = BillableHourSchema()
        employee_bills_list = billable_schema.dump(BillableHourModel.query.filter_by(id=emp_id).all(), many=True)
        return make_response(jsonify(employee_bills_list))

    def get_employee_company_bills(self, emp_id, company):
        """
        Retrieve specific bill
        """
        billable_schema = BillableHourSchema()
        employee_company_bill = billable_schema.dump(BillableHourModel.query.filter_by(id=emp_id, company=company).first())
        return make_response(jsonify(employee_company_bill))

    def get_company_bills(self, company):
        """
        Retrieve bills of specific company
        """
        company_bills = defaultdict(list)
        total_bill_cost = 0
        get_bill_list = BillableHourModel.query.filter_by(company=company).all()
        for each_bill in get_bill_list:
            start_time = list(map(int, str(each_bill.start_time).split(':')))
            end_time = list(map(int, str(each_bill.end_time).split(':')))
            for index in range(len(start_time)):
                if index == 0:
                    hours_worked = end_time[index] - start_time[index]
                elif index == 1:
                    if start_time[index] > end_time[index]:
                        minutes_worked = start_time[index] - end_time[index]
                    else:
                        minutes_worked = end_time[index] - start_time[index]
                    time_worked = round(hours_worked + (minutes_worked / 60), 2)
            total_rate = round(time_worked * each_bill.billable_rate, 2)
            total_bill_cost += total_rate
            company_bills[each_bill.company].append({
                "Employee ID": each_bill.id,
                "Number Of Hours": time_worked,
                "Unit Price": each_bill.billable_rate,
                "Cost": total_rate,
            })
        company_bills[company].append({"Total": total_bill_cost})
        return make_response(company_bills)




























# from flask import request
# from app import db
# # from models.Client import Client
#
#
# class CreateBill:
#     def create_bill(self):
#         employeeID = request.form['employeeID']  # submit employeeID
#         billableRate = request.form['billableRate']  # submit billableRate
#         company = request.form['company']  # submit company
#         date = request.form['date']  # submit date
#         startTime = request.form['startTime']  # submit time started
#         endTime = request.form['endTime']  # sumbit end time
#
#         # @@TODO: return clientDetails in a more dynamic form as to string for further processing.
#
#         client = Client(employeeID=employeeID, billableRate=billableRate, company=company,
#                         date=date, startTime=startTime, endTime=endTime)  # pass data from lawyer to Client Model
#         db.session.add(client)  # session -> clientdatabase.db
#         db.session.commit()  # commit to clientdatabase.db
#         return 'Data passed to clientdatabase.db'
#
#     # return 'TimeSheet Created:\n' +  'Details:' + str(clientDetails) # return data captured.
#     pass
#
#
# class ReadBill:
#     pass
#
#
# class UpdateBill:
#     pass
#
#
# class DeleteBill:
#     pass