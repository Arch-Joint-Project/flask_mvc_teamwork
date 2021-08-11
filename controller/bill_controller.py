# third party imports
from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

# local imports
from models.model import BillableHourModel, BillableHourSchema
from app import db

# builtin imports
from collections import defaultdict


class Bill:
    """
    The bill class handles requests in relations to lawyers
    creating, reading, updating and deleting bills
    """
    def __init__(self):
        pass

    def get_bills(self):
        """
        Retrieve bills from the database
        :return:
        """
        if request.method == 'GET':
            if not request.args:
                return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
            else:
                if 'company' in request.args and 'emp_id' in request.args:
                    """
                    Retrieve specific bill of a lawyer for a specific company
                    """
                    billable_schema = BillableHourSchema()
                    employee_company_bill = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                        'emp_id'), company=request.args.get('company')).first())
                    return make_response(jsonify(employee_company_bill))
                elif 'emp_id' in request.args:
                    """
                    Retrieve bills of a specific lawyer
                    """
                    billable_schema = BillableHourSchema()
                    employee_bills_list = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                        'emp_id')).all(), many=True)
                    return make_response(jsonify(employee_bills_list))
                else:
                    return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))
        else:
            return make_response(jsonify({'status': 'error', 'error': 'invalid request'}))

    def create_bill(self):
        """
        Create bill for specific company
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
                return make_response(jsonify({'status': 'error', 'error': 'error inserting data'}))
        else:
            return make_response(jsonify({'status': 'error', 'error': 'invalid request'}))

    def update_bill(self):
        """
        Update specific bill
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
            return make_response(jsonify({'status': 'error', 'error': 'invalid request'}))

    def delete_bill(self):
        """
        Delete bill from database
        :return:
        """
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
                elif 'emp_id' in request.args:
                    """
                    Delete specific lawyer bills
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
    """
    The accounts class handles request in relations to
    operations performed by accounts officers
    """
    def __init__(self):
        pass

    def generate_invoice(self):
        """
        Generate invoice
        :return:
        """
        if request.method == 'GET':
            if not request.args:
                return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
            else:
                if 'company' in request.args:
                    """
                    Generate invoice for company
                    """
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
                    return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))
        else:
            return make_response(jsonify({'status': 'error', 'error': 'invalid request'}))
