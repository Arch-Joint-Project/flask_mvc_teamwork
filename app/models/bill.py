# local import
from app import db, ma


class BillableHourModel(db.Model):
    """
    Table schema for recording bills
    """
    __tablename__ = 'billing_db'
    id = db.Column('Employee ID', db.Integer, primary_key=True)
    billable_rate = db.Column('Billable Rate (per hour)', db.Integer, nullable=False)
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
        fields = ('id', 'company', 'billable_rate', 'date', 'start_time', 'end_time')