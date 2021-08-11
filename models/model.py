# local import
from app import db, ma


class BillableHourModel(db.Model):
    """
    Table schema for recording bills
    """
    __tablename__ = 'billing_hours'
    id = db.Column('Employee ID', db.Integer, primary_key=True)
    billable_rate = db.Column('Billable Rare (per hour)', db.Integer, nullable=False)
    company = db.Column('Company', db.String(60), primary_key=True)
    date = db.Column('Date', db.Date())
    start_time = db.Column('Start Time', db.Time())
    end_time = db.Column('End Time', db.Time())

    def __init__(self, employee_id, billable_rate, company, date, start_time, end_time):
        self.id = employee_id
        self.billable_rate = billable_rate
        self.company = company
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"<Company {self.company}>"


class BillableHourSchema(ma.Schema):
    """
    Marshmallow schema for serialization
    """
    class Meta:
        """
        Fields to expose
        """
        fields = ('id', 'company', 'billable_rate', 'date')

























# # from flask_sqlalchemy import SQLAlchemy
# from app import db
# # db = SQLAlchemy()
#
#
# class Client(db.Model):
#         __tablename__ = 'clients'
#         recordID = db.Column(db.Integer, primary_key=True, nullable=False)
#         employeeID = db.Column(db.Integer, nullable=False)
#         billableRate = db.Column(db.Integer, nullable=False)
#         company = db.Column(db.String(50), nullable=False)
#         date = db.Column(db.Text, nullable=False)
#         startTime = db.Column(db.Text, nullable=False)
#         endTime = db.Column(db.Text, nullable=False)
#
#         @property
#         def serialize(self):
#                 return {
#                         'recordID': self.recordID,
#                         'employeeID': self.employeeID,
#                         'billableRate': self.billableRate,
#                         'company': self.company,
#                         'date': self.date,
#                         'startTime': self.startTime,
#                         'endTime':self.endTime
#                 }