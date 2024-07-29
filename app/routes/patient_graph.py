from flask import request
from flask_restful import Resource, reqparse
from py2neo import Graph, Node, Relationship

from app.models.doctor_model import Doctor
from app.models.employee_model import Employee
from app.models.insurance_claim_model import InsuranceClaim
from app.models.inventory_model import InventoryItem
from app.models.invoice_model import Invoice
from app.models.patient_model import Patient

from app import db

class PatientGraph(Resource):
    def post(self):
        data = request.get_json()
        patient_id = data.get('patient_id')
        if not patient_id:
            return {"message": "Patient ID is required"}, 400

        graph = Graph("bolt://localhost:7687", auth=("", ""))

        # Clear existing graph
        graph.run("MATCH (n) DETACH DELETE n")

        nodes = {}
        relationships = []

        # Insert the patient node and its relationships
        self.insert_patient_graph(graph, patient_id, nodes, relationships)

        # Convert the data to the required JSON format
        graph_data = {
            "nodes": list(nodes.values()),
            "edges": relationships
        }
        return graph_data

    def insert_patient_graph(self, graph, patient_id, nodes, relationships):
        patient = Patient.query.get(patient_id)
        patient_object = patient.to_dict() if patient else None
        if not patient:
            return

        # Insert patient node
        patient_node = Node("Patient Name: "+patient_object["name"], id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
        graph.create(patient_node)
        nodes[patient.id] = {
            "id": patient_node.identity,
            "label": "Patient",
            "properties": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "diagnosis": patient.diagnosis,
                "treatment": patient.treatment
            }
        }

        # Insert relationships with doctor
        if patient.doctor_id:
            doctor = Doctor.query.get(patient.doctor_id)
            doctor_object = doctor.to_dict() if doctor else None
            doctor_node = Node(doctor_object["name"], id=doctor.id, name=doctor.name, specialty=doctor.specialty)
            graph.merge(doctor_node, "Doctor", "id")
            relationship = Relationship(patient_node, "TREATED_BY", doctor_node)
            graph.create(relationship)
            nodes[doctor.id] = {
                "id": doctor_node.identity,
                "label": "Doctor",
                "properties": {
                    "id": doctor.id,
                    "name": doctor.name,
                    "specialty": doctor.specialty
                }
            }
            relationships.append({
                "id": relationship.identity,
                "source": patient_node.identity,
                "target": doctor_node.identity,
                "label": "TREATED_BY",
                "properties": {}
            })

        # Insert relationships with invoices
        invoices = Invoice.query.filter_by(patient_id=patient_id).all()
        for invoice in invoices:
            id = str(invoice.id)
            invoice_node = Node("Invoice Id: "+id, id=invoice.id, amount=invoice.amount, description=invoice.description)
            graph.create(invoice_node)
            nodes[invoice.id] = {
                "id": invoice_node.identity,
                "label": "Invoice",
                "properties": {
                    "id": invoice.id,
                    "amount": invoice.amount,
                    "description": invoice.description
                }
            }
            relationship = Relationship(invoice_node, "ISSUED_TO", patient_node)
            graph.create(relationship)
            relationships.append({
                "id": relationship.identity,
                "source": invoice_node.identity,
                "target": patient_node.identity,
                "label": "ISSUED_TO",
                "properties": {}
            })

        # Insert relationships with insurance claims
        insurance_claims = InsuranceClaim.query.filter_by(patient_id=patient_id).all()
        for claim in insurance_claims:
            id = str(claim.id)
            claim_node = Node("InsuranceClaim ID: "+ id, id=claim.id, amount=claim.amount, status=claim.status)
            graph.create(claim_node)
            nodes[claim.id] = {
                "id": claim_node.identity,
                "label": "InsuranceClaim",
                "properties": {
                    "id": claim.id,
                    "amount": claim.amount,
                    "status": claim.status
                }
            }
            relationship = Relationship(claim_node, "BELONGS_TO", patient_node)
            graph.create(relationship)
            relationships.append({
                "id": relationship.identity,
                "source": claim_node.identity,
                "target": patient_node.identity,
                "label": "BELONGS_TO",
                "properties": {}
            })

        # Insert relationships with employees (example, assuming some connection)
        employees = Employee.query.filter(Employee.id == patient.doctor_id).all()
        for employee in employees:
            id = str(employee.id)
            employee_node = Node("Employee ID: "+id, id=employee.id, name=employee.name, role=employee.role, department=employee.department)
            graph.create(employee_node)
            nodes[employee.id] = {
                "id": employee_node.identity,
                "label": "Employee",
                "properties": {
                    "id": employee.id,
                    "name": employee.name,
                    "role": employee.role,
                    "department": employee.department
                }
            }
            relationship = Relationship(employee_node, "WORKS_WITH", patient_node)
            graph.create(relationship)
            relationships.append({
                "id": relationship.identity,
                "source": employee_node.identity,
                "target": patient_node.identity,
                "label": "WORKS_WITH",
                "properties": {}
            })
