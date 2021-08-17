# third party imports
from flask import request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError

# local imports
from app.models.bill import BillableHourModel, BillableHourSchema
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

        if 'company' in request.args and 'emp_id' in request.args:
            """
            Retrieve specific bill of a lawyer for a specific company
            """
            billable_schema = BillableHourSchema()
            employee_company_bill = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                'emp_id'), company=request.args.get('company').lower()).first())
            if employee_company_bill:
                return make_response(jsonify(employee_company_bill))
            else:
                return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
        elif 'emp_id' in request.args:
            """
            Retrieve bills of a specific lawyer
            """
            billable_schema = BillableHourSchema()
            employee_bills_list = billable_schema.dump(BillableHourModel.query.filter_by(id=request.args.get(
                'emp_id')).all(), many=True)
            if employee_bills_list:
                return make_response(jsonify(employee_bills_list))
            else:
                return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))

        else:
            return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))

    def create_bill(self):
        """
        JSON
        Create bill for specific company
        :return:
        """
        bill_info = request.get_json()
        bill_info["company"] = bill_info["company"].lower()
        try:
            bill = BillableHourModel(**bill_info)
            db.session.add(bill)
            db.session.commit()
            return make_response(jsonify(bill_info))
        except SQLAlchemyError as e:
            return make_response(jsonify({'status': 'error', 'error': 'error inserting data'}))

    # def create_bill(self):
    #     """
    #       form-data
    #     Create bill for specific company
    #     """
    #     bill_info = request.form
    #     try:
    #         bill = BillableHourModel(
    #             employee_id=bill_info['employee_id'],
    #             billable_rate=bill_info['billable_rate'],
    #             company=bill_info['company'],
    #             date=bill_info['date'],
    #             start_time=bill_info['start_time'],
    #             end_time=bill_info['end_time']
    #         )
    #         db.session.add(bill)
    #         db.session.commit()
    #         return make_response(jsonify(bill_info))
    #     except SQLAlchemyError as e:
    #         return make_response(jsonify({'status': 'error', 'error': 'error inserting data'}))

    def update_bill(self):
        """
        json
        Update specific bill
        """
        if not request.args:
            return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
        else:
            if 'company' in request.args and 'emp_id' in request.args:
                bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id'),
                                                              company=request.args.get('company').lower())
                if bill_info:
                    bill_info.update(request.get_json())
                    db.session.commit()
                    return make_response(jsonify({'status': 'successful', 'msg': 'resource updated'}))
                else:
                    return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
            else:
                return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))

    # def update_bill(self):
    #     """
    #      form-data
    #     Update specific bill
    #     """
    #     if not request.args:
    #         return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
    #     else:
    #         if 'company' in request.args and 'emp_id' in request.args:
    #             form_data = dict(request.form)
    #             print(f'dict is {form_data}')
    #             bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id'),
    #                                                           company=request.args.get('company').lower())
    #             if bill_info:
    #                 bill_info.update(form_data)
    #                 db.session.commit()
    #                 return make_response(jsonify({'status': 'successful', 'msg': 'resource updated'}))
    #             else:
    #                 return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
    #         else:
    #             return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))

    def delete_bill(self):
        """
        Delete bill from database
        :return:
        """
        if not request.args:
            return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))

        else:
            if 'company' in request.args and 'emp_id' in request.args:
                """
                Delete a specific bill
                """
                bill_info = BillableHourModel.query.filter_by(id=request.args.get('emp_id'),
                                                              company=request.args.get('company').lower()).first()
                if bill_info:
                    db.session.delete(bill_info)
                    db.session.commit()
                    return make_response(jsonify({'status': 'successful', 'msg': 'resource deleted'}))
                else:
                    return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
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
                    return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
            else:
                return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))


class Accounts:
    """
    The accounts class handles request in relations to
    operations performed by accounts officers.
    Getting Total bill cost for a specific company
    """

    def __init__(self):
        pass

    def generate_invoice(self):
        """
        Generate invoice
        :return:
        """
        if not request.args:
            return make_response(jsonify({'status': 'error', 'error': 'no parameter provided'}))
        else:
            if 'company' in request.args:
                """
                Generate invoice for company
                """
                company_bills = defaultdict(list)
                total_bill_cost = 0
                get_bill_list = BillableHourModel.query.filter_by(company=request.args.get('company').lower()).all()
                if get_bill_list:
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
                    return make_response(jsonify({'status': 'error', 'error': 'requested resource was not found'}))
            else:
                return make_response(jsonify({'status': 'error', 'error': 'invalid parameter'}))