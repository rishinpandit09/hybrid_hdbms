from app import db


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialty = db.Column(db.String(100))
    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'patients': [patient.to_dict() for patient in self.patients] if self.patients else []
        }