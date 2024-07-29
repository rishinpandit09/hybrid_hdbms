from flask import request, jsonify
from flask_restful import Resource
from app.models import db, doctor_model
from app.memgraph import insert_doctor_to_memgraph


class DoctorListResource(Resource):
    def get(self):
        doctors = Doctor.query.all()
        return jsonify([doctor.to_dict() for doctor in doctors])

    def post(self):
        data = request.get_json()
        new_doctor = Doctor(
            name=data['name'],
            specialty=data['specialty']
        )
        db.session.add(new_doctor)
        db.session.commit()

        # Insert into Memgraph
        insert_doctor_to_memgraph(
            doctor_id=new_doctor.id,
            name=new_doctor.name,
            specialty=new_doctor.specialty
        )

        return jsonify({'message': 'Doctor added', 'doctor': new_doctor.id})


class DoctorResource(Resource):
    def get(self, id):
        doctor = Doctor.query.get_or_404(id)
        return jsonify(doctor.to_dict())

    def put(self, id):
        data = request.get_json()
        doctor = Doctor.query.get_or_404(id)
        doctor.name = data['name']
        doctor.specialty = data['specialty']
        db.session.commit()
        return jsonify({'message': 'Doctor updated', 'doctor': doctor.id})

    def delete(self, id):
        doctor = Doctor.query.get_or_404(id)
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({'message': 'Doctor deleted', 'doctor': id})
