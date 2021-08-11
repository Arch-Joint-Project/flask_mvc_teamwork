# third party imports
from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

# local imports
from models.model import BillableHourModel, BillableHourSchema
from app import db

# builtin imports
from collections import defaultdict


class Bill:
    def __init__(self):
        pass

    def get_bills(self):
        """
        Retrieve all available bills
        """
        print('get bills')
        if not request.args:
            print('no args')
            billable_schema = BillableHourSchema()
            bills = billable_schema.dump(BillableHourModel.query.all(), many=True)
            return make_response(jsonify(bills))
        else:
            if 'company' in request.args and 'emp_id' in request.args:
                print('both available')
                """
                Retrieve specific bill
                """
                billable_schema = BillableHourSchema()
                employee_company_bill = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                    'emp_id'), company=request.args.get('company')).first())
                return make_response(jsonify(employee_company_bill))
            elif 'emp_id' in request.args:
                print('id available')
                """
                Retrieve bills of a specific employee
                """
                billable_schema = BillableHourSchema()
                employee_bills_list = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                    'emp_id')).all(), many=True)
                return make_response(jsonify(employee_bills_list))
            elif 'company' in request.args:
                """
                Retrieve bills of specific company
                """
                print(request.args)
                company_bills = defaultdict(list)
                total_bill_cost = 0
                get_bill_list = BillableHourModel.query.filter_by(company=request.args.get('company')).all()
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
                company_bills[request.args.get('company')].append({"Total": total_bill_cost})
                return make_response(company_bills)
            else:
                print(request.args.keys())
                return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))

    def create_bill(self):
        """
        Create bills for various companies
        """
        print('post')
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
                return make_response(jsonify({'status': 'error', 'error': 'Error Inserting Data'}))
        else:
            return make_response(jsonify({'status' : 'error', 'error': 'Invalid Request'}))

    def update_bill(self):
        """
        Update bill of a specific company
        """
        if request.method == 'PUT':
            if not request.args:
                return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
            else:
                if 'company' in request.args and 'emp_id' in request.args:
                    bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id'),
                                                                  company=request.args.get('company')).first()
                    if bill_info:
                        bill_info.date = request.form['date']
                        bill_info.start_time = request.form['start_time']
                        bill_info.end_time = request.form['end_time']
                        bill_info.billable_rate = request.form['billable_rate']
                        db.session.commit()
                        return make_response(jsonify({'status': 'successful', 'msg': 'resource updated'}))
                    else:
                        return make_response(jsonify({'status': 'error', 'error': 'records not found'}))
                else:
                    return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))
        else:
            return make_response(jsonify({'status': 'error', 'error': 'Invalid Request'}))

    def delete_bill(self):
        print('delete')
        if request.method == 'DELETE':
            if not request.args:
                return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
            else:
                if 'company' in request.args and 'emp_id' in request.args:
                    """
                    Delete a specific bill
                    """
                    bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id'),
                                                              company=request.args.get('company')).first()
                    if bill_info:
                        db.session.delete(bill_info)
                        db.session.commit()
                        return make_response(jsonify({'status': 'successful', 'msg': 'resource deleted'}))
                    else:
                        return make_response(jsonify({'status': 'error', 'error': 'record not found'}))
                elif 'company' in request.args:
                    """
                    Delete specific company bill
                    """
                    bill_info = BillableHourModel.query.filter_by(company=request.args.get('company')).all()
                    if bill_info:
                        for bill in bill_info:
                            db.session.delete(bill)
                            db.session.commit()
                        return make_response(jsonify({'status': 'success', 'msg': 'resource deleted'}))
                    else:
                        return make_response(jsonify({'status': 'error', 'error': 'record not found'}))
                elif 'emp_id' in request.args:
                    """
                    Delete specific employee bills
                    """
                    bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id')).all()
                    if bill_info:
                        for bill in bill_info:
                            db.session.delete(bill)
                            db.session.commit()
                        return make_response(jsonify({'status': 'success', 'msg': 'resource deleted'}))
                    else:
                        return make_response(jsonify({'status': 'error', 'error': 'record not found'}))
                else:
                    return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))
        else:
            return make_response(jsonify({'status': 'error', 'error': 'invalid request'}))


class Accounts:
    def __init__(self):
        pass

    def generate_invoice(self):
        if not request.args:
            return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
        else:
            if 'company' in request.args:
                """
                Generate invoice for company
                """
                print(request.args)
                company_bills = defaultdict(list)
                total_bill_cost = 0
                get_bill_list = BillableHourModel.query.filter_by(company=request.args.get('company')).all()
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
                company_bills[request.args.get('company')].append({"Total": total_bill_cost})
                return make_response(company_bills)
