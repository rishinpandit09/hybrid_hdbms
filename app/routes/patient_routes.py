from flask_restful import Resource, reqparse
from app.models.patient_model import Patient
from app import db

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('age', type=int, required=True, help='Age cannot be blank')
parser.add_argument('diagnosis', type=str)
parser.add_argument('treatment', type=str)


class PatientListResource(Resource):
    def get(self):
        patients = Patient.query.all()
        return [patient.to_dict() for patient in patients], 200

    def post(self):
        args = parser.parse_args()
        new_patient = Patient(
            name=args['name'],
            age=args['age'],
            diagnosis=args.get('diagnosis'),
            treatment=args.get('treatment')
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient.to_dict(), 201


class PatientResource(Resource):
    def get(self, id):
        patient = Patient.query.get_or_404(id)
        return patient.to_dict(), 200

    def put(self, id):
        args = parser.parse_args()
        patient = Patient.query.get_or_404(id)
        patient.name = args.get('name', patient.name)
        patient.age = args.get('age', patient.age)
        patient.diagnosis = args.get('diagnosis', patient.diagnosis)
        patient.treatment = args.get('treatment', patient.treatment)
        db.session.commit()
        return patient.to_dict(), 200

    def delete(self, id):
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        return '', 204
