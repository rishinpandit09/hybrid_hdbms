# app/routes/patient_routes.py
from flask import jsonify
from flask_restful import Resource, reqparse
from app.models.patient_model import Patient
from app import db
from memgraph import insert_patient_to_memgraph

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

        # Insert into Memgraph
        insert_patient_to_memgraph(
            patient_id=new_patient.id,
            name=new_patient.name,
            age=new_patient.age,
            diagnosis=new_patient.diagnosis,
            treatment=new_patient.treatment,
            doctor_id=new_patient.doctor_id
        )

        return jsonify({'message': 'Patient added', 'patient': new_patient.id}), 201


# app/routes/patient_routes.py (continued)
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

        # # Update in Memgraph
        # if memgraph:
        #     query = (
        #         'MATCH (n:Patient) WHERE n.id = $id '
        #         'SET n.name = $name, n.age = $age, n.diagnosis = $diagnosis, n.treatment = $treatment '
        #         'RETURN n'
        #     )
        #     params = {
        #         'id': id,
        #         'name': args.get('name'),
        #         'age': args.get('age'),
        #         'diagnosis': args.get('diagnosis'),
        #         'treatment': args.get('treatment')
        #     }
        #     memgraph.execute_and_fetch(query, params)

        return patient.to_dict(), 200

    def delete(self, id):
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()

        # # Delete from Memgraph
        # if memgraph:
        #     query = 'MATCH (n:Patient) WHERE n.id = $id DELETE n'
        #     params = {'id': id}
        #     memgraph.execute_and_fetch(query, params)

        return '', 204
