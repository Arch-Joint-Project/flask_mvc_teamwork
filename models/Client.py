from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Client(db.Model):
        recordID = db.Column(db.Integer, primary_key=True, nullable=False)
        employeeID = db.Column(db.Integer, nullable=False)
        billableRate = db.Column(db.Integer, nullable=False)
        company = db.Column(db.String(50), nullable=False)
        date = db.Column(db.Text, nullable=False)
        startTime = db.Column(db.Text, nullable=False)
        endTime = db.Column(db.Text, nullable=False)

        @property
        def serialize(self):
                return {
                        'recordID': self.recordID,
                        'employeeID': self.employeeID,
                        'billableRate': self.billableRate,
                        'company': self.company,
                        'date': self.date,
                        'startTime': self.startTime,
                        'endTime':self.endTime
                }