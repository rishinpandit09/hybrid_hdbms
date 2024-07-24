from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)


    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'patient_id': self.patient_id,
    #         'amount': self.amount,
    #         'description': self.description
    #     }
